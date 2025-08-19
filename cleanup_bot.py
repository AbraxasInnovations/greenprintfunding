#!/usr/bin/env python3
"""
Cleanup script for the Abraxas Greenprint Funding Bot.
This script ensures no bot instances are running before starting a new one.
"""

import os
import sys
import time
import logging
import subprocess
import signal
import psutil
import argparse

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot process identifiers - patterns to search for in command lines
BOT_PROCESS_PATTERNS = [
    'telegram_bot.py',
    'python-telegram-bot',
    'bot_service.py',
    'arb_bot.py',
    'crypto-arb-bot'
]

def find_bot_processes():
    """Find all running bot processes using multiple detection methods."""
    bot_processes = []
    
    # Method 1: Using psutil to find python processes with bot-related command lines
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Check if this is a bot process based on command line
            cmdline = proc.info['cmdline']
            if cmdline:
                cmdline_str = ' '.join(cmdline)
                for pattern in BOT_PROCESS_PATTERNS:
                    if pattern in cmdline_str:
                        bot_processes.append(proc)
                        logger.info(f"Found bot process: PID={proc.pid}, CMD={cmdline_str}")
                        break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            logger.debug(f"Error accessing process info: {str(e)}")
        except Exception as e:
            logger.warning(f"Unexpected error checking process: {str(e)}")
    
    # Method 2: Using 'ps' command as a fallback
    try:
        ps_patterns = '|'.join(BOT_PROCESS_PATTERNS)
        ps_command = f"ps aux | grep -E '{ps_patterns}' | grep -v grep"
        
        result = subprocess.run(ps_command, shell=True, capture_output=True, text=True)
        if result.stdout.strip():
            # Parse the output to get PIDs
            for line in result.stdout.strip().split('\n'):
                fields = line.split()
                if len(fields) > 1:
                    try:
                        pid = int(fields[1])
                        # Check if we already found this process
                        if not any(p.pid == pid for p in bot_processes):
                            try:
                                proc = psutil.Process(pid)
                                bot_processes.append(proc)
                                logger.info(f"Found additional bot process via ps: PID={pid}, User={fields[0]}")
                            except psutil.NoSuchProcess:
                                logger.debug(f"Process {pid} no longer exists")
                    except (ValueError, IndexError):
                        logger.debug(f"Could not parse PID from ps output line: {line}")
    except Exception as e:
        logger.warning(f"Error using ps command fallback: {str(e)}")
    
    return bot_processes

def stop_process(process, dry_run=False):
    """Stop a process gracefully, then forcefully if needed."""
    try:
        pid = process.pid
        cmdline = ' '.join(process.cmdline()) if hasattr(process, 'cmdline') else str(process)
        
        if dry_run:
            logger.info(f"[DRY RUN] Would stop process {pid}: {cmdline}")
            return True, "Would have been stopped (dry run)"
        
        logger.info(f"Stopping process {pid}: {cmdline}")
        process.terminate()
        
        # Wait for graceful termination
        for _ in range(10):  # Wait up to 5 seconds (10 * 0.5s)
            time.sleep(0.5)
            try:
                # Check if process still exists
                if not psutil.pid_exists(pid) or process.status() == psutil.STATUS_ZOMBIE:
                    logger.info(f"Process {pid} terminated gracefully")
                    return True, "Terminated gracefully"
            except psutil.NoSuchProcess:
                logger.info(f"Process {pid} terminated gracefully")
                return True, "Terminated gracefully"
        
        # Force kill if still running
        logger.warning(f"Process {pid} did not terminate gracefully, forcing kill")
        try:
            # Try SIGKILL
            process.kill()
        except psutil.NoSuchProcess:
            logger.info(f"Process {pid} already terminated")
            return True, "Already terminated"
        
        # Verify kill
        for _ in range(5):  # Wait up to 2.5 seconds (5 * 0.5s)
            time.sleep(0.5)
            try:
                # Check if process still exists
                if not psutil.pid_exists(pid) or process.status() == psutil.STATUS_ZOMBIE:
                    logger.info(f"Process {pid} killed successfully")
                    return True, "Killed forcefully"
            except psutil.NoSuchProcess:
                logger.info(f"Process {pid} killed successfully")
                return True, "Killed forcefully"
        
        # Extra kill attempt using os.kill for more direct approach
        try:
            logger.warning(f"Process {pid} still running, trying direct OS kill")
            os.kill(pid, signal.SIGKILL)
            time.sleep(1)
            if not psutil.pid_exists(pid):
                logger.info(f"Process {pid} killed successfully with direct OS kill")
                return True, "Killed with direct OS kill"
        except ProcessLookupError:
            logger.info(f"Process {pid} already terminated during direct kill attempt")
            return True, "Already terminated during direct kill"
        except Exception as e:
            logger.error(f"Error during direct kill of process {pid}: {str(e)}")
        
        logger.error(f"Failed to kill process {pid} even with force kill")
        return False, "Failed to kill"
    
    except psutil.NoSuchProcess:
        logger.info(f"Process {pid} already stopped")
        return True, "Already stopped"
    except Exception as e:
        logger.error(f"Error stopping process {pid}: {str(e)}")
        return False, f"Error: {str(e)}"

def verify_cleanup():
    """Verify that cleanup was successful and no bot processes remain."""
    remaining = find_bot_processes()
    
    if remaining:
        logger.error(f"Verification failed: {len(remaining)} bot processes still running")
        for proc in remaining:
            try:
                cmdline = ' '.join(proc.cmdline()) if hasattr(proc, 'cmdline') else str(proc)
                logger.error(f"Still running: PID={proc.pid}, CMD={cmdline}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                logger.error(f"Still running: PID={proc.pid}, CMD=<access denied>")
        return False, remaining
    
    logger.info("Verification successful: No bot processes remain")
    return True, []

def main(dry_run=False):
    """Main cleanup function.
    
    Args:
        dry_run: If True, only log what would be done without actually stopping processes
        
    Returns:
        tuple: (success, details)
            - success (bool): True if cleanup was successful, False otherwise
            - details (dict): Dictionary with information about the operation
    """
    logger.info(f"Starting bot cleanup{' (DRY RUN)' if dry_run else ''}...")
    
    # Find all bot processes
    bot_processes = find_bot_processes()
    logger.info(f"Found {len(bot_processes)} running bot instances")
    
    # Track results
    results = {
        'total_found': len(bot_processes),
        'stopped': 0,
        'failed': 0,
        'failed_details': [],
        'remaining': 0,
        'remaining_pids': []
    }
    
    # Stop each process
    for proc in bot_processes:
        success, result_msg = stop_process(proc, dry_run)
        
        if success:
            results['stopped'] += 1
            logger.debug(f"Successfully stopped PID {proc.pid}: {result_msg}")
        else:
            results['failed'] += 1
            details = {
                'pid': proc.pid,
                'reason': result_msg
            }
            try:
                details['cmdline'] = ' '.join(proc.cmdline())
            except:
                pass
            results['failed_details'].append(details)
            logger.error(f"Failed to stop PID {proc.pid}: {result_msg}")
    
    # Verify cleanup
    if not dry_run:
        verification_success, remaining_processes = verify_cleanup()
        results['verification_success'] = verification_success
        results['remaining'] = len(remaining_processes)
        results['remaining_pids'] = [p.pid for p in remaining_processes]
        
        if not verification_success:
            logger.error(f"Failed to stop {len(remaining_processes)} bot instances")
            for proc in remaining_processes:
                try:
                    cmdline = ' '.join(proc.cmdline()) if hasattr(proc, 'cmdline') else "<unknown>"
                    logger.error(f"Still running: PID={proc.pid}, CMD={cmdline}")
                except:
                    logger.error(f"Still running: PID={proc.pid}, CMD=<could not retrieve>")
            
            # Return details of failure
            return False, results
    else:
        results['verification_success'] = None  # Not applicable in dry run
        logger.info("[DRY RUN] Skipping verification step")
    
    # Final status message
    if dry_run:
        logger.info(f"[DRY RUN] Would have stopped {results['total_found']} bot processes")
    else:
        logger.info(f"Successfully stopped {results['stopped']} bot instances")
        logger.info("Cleanup completed successfully")
    
    return True, results

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Cleanup Abraxas Greenprint Funding Bot processes')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without actually stopping processes')
    args = parser.parse_args()
    
    # Run the cleanup
    success, details = main(dry_run=args.dry_run)
    
    # Exit with appropriate code
    if not success:
        sys.exit(1) 
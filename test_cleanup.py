#!/usr/bin/env python3
"""
Test script for cleanup_bot.py
This script creates mock bot processes and then tests if cleanup_bot.py can find and terminate them.
"""

import os
import sys
import time
import logging
import subprocess
import signal
import psutil
import argparse
import threading
import tempfile
import atexit
import cleanup_bot

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global list to track mock processes
mock_processes = []
mock_process_files = []

def create_mock_script(name, sleep_time=60):
    """Create a temporary Python script that will run as a mock bot process."""
    temp_file = tempfile.NamedTemporaryFile(prefix=f"mock_{name}_", suffix=".py", delete=False)
    
    script_content = f"""#!/usr/bin/env python3
# Mock {name} process for testing cleanup_bot.py
import time
import sys
import signal
import os

def signal_handler(sig, frame):
    print('Signal received, exiting gracefully')
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

print(f"Mock {name} started with PID {{os.getpid()}}")
try:
    while True:
        # simulate running bot
        time.sleep(1)
        sys.stdout.flush()
except KeyboardInterrupt:
    pass
print(f"Mock {name} shutting down")
"""
    
    temp_file.write(script_content.encode('utf-8'))
    temp_file.close()
    os.chmod(temp_file.name, 0o755)  # Make executable
    mock_process_files.append(temp_file.name)
    return temp_file.name

def start_mock_process(script_path, process_name):
    """Start a mock bot process."""
    cmd = [sys.executable, script_path]
    logger.info(f"Starting mock process: {' '.join(cmd)}")
    
    # Use a different process group to avoid the cleanup killing our test script
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        start_new_session=True
    )
    
    # Wait for startup message
    for _ in range(5):  # Try for up to 5 seconds
        if process.poll() is not None:
            logger.error(f"Mock process failed to start: {process.stdout.read()}")
            return None
        
        line = process.stdout.readline()
        if line and "started with PID" in line:
            logger.info(line.strip())
            mock_processes.append(process)
            return process
        
        time.sleep(1)
    
    logger.warning(f"Mock process started but didn't produce expected output")
    mock_processes.append(process)
    return process

def cleanup_mock_files():
    """Clean up temp files."""
    for file_path in mock_process_files:
        try:
            os.unlink(file_path)
            logger.debug(f"Removed temporary file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to remove temporary file {file_path}: {str(e)}")

def forcefully_terminate_mock_processes():
    """Forcefully terminate any remaining mock processes to ensure cleanup."""
    for process in mock_processes:
        try:
            if process.poll() is None:  # Still running
                process.terminate()
                time.sleep(0.5)
                if process.poll() is None:
                    process.kill()
                    logger.warning(f"Forcefully killed mock process PID {process.pid}")
                else:
                    logger.info(f"Terminated mock process PID {process.pid}")
        except Exception as e:
            logger.warning(f"Error terminating mock process: {str(e)}")

def main():
    """Run the cleanup bot test."""
    # Register cleanup handlers
    atexit.register(forcefully_terminate_mock_processes)
    atexit.register(cleanup_mock_files)
    
    # Parse arguments
    parser = argparse.ArgumentParser(description='Test cleanup_bot.py with mock processes')
    parser.add_argument('--num-processes', type=int, default=3, 
                       help='Number of mock processes to create (default: 3)')
    args = parser.parse_args()
    
    logger.info(f"Starting cleanup_bot.py test with {args.num_processes} mock processes")
    
    # Create and start mock processes
    process_types = ["telegram_bot.py", "bot_service.py", "arb_bot.py"]
    started_processes = []
    
    for i in range(args.num_processes):
        process_type = process_types[i % len(process_types)]
        script_path = create_mock_script(process_type)
        process = start_mock_process(script_path, process_type)
        if process:
            started_processes.append(process)
    
    if not started_processes:
        logger.error("Failed to start any mock processes, aborting test")
        return False
    
    logger.info(f"Started {len(started_processes)} mock processes")
    
    # Give processes time to fully initialize
    time.sleep(2)
    
    # Verify the processes are found by the find_bot_processes function
    bot_processes = cleanup_bot.find_bot_processes()
    logger.info(f"cleanup_bot.py found {len(bot_processes)} bot processes")
    
    for proc in bot_processes:
        try:
            cmdline = ' '.join(proc.cmdline())
            logger.info(f"Found: PID={proc.pid}, CMD={cmdline}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            logger.info(f"Found: PID={proc.pid}, CMD=<access denied>")
    
    # Run the cleanup script
    logger.info("Running cleanup_bot.py...")
    success, details = cleanup_bot.main(dry_run=False)
    
    # Check results
    if success:
        logger.info("Cleanup successful!")
        logger.info(f"Details: {details}")
    else:
        logger.error("Cleanup failed!")
        logger.error(f"Details: {details}")
    
    # Verify no processes remain
    time.sleep(1)  # Give processes time to fully terminate
    remaining = cleanup_bot.find_bot_processes()
    
    if remaining:
        logger.error(f"Test failed: {len(remaining)} processes still running after cleanup")
        for proc in remaining:
            try:
                cmdline = ' '.join(proc.cmdline())
                logger.error(f"Still running: PID={proc.pid}, CMD={cmdline}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                logger.error(f"Still running: PID={proc.pid}, CMD=<access denied>")
        return False
    else:
        logger.info("Test passed: All mock processes were successfully terminated")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
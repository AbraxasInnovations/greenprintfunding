#!/usr/bin/env python3
"""
Cleanup script for Abraxas Greenprint Bot
----------------------------------------
This script helps clean up any running bot instances before starting a new one.
"""

import os
import sys
import subprocess
import logging

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def cleanup_bot():
    """Clean up any running bot instances"""
    try:
        # Find Python processes that might be running the bot
        cmd = "ps aux | grep python | grep -v grep"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            processes = result.stdout.split('\n')
            bot_processes = [p for p in processes if 'telegram_bot.py' in p]
            
            if bot_processes:
                logger.info(f"Found {len(bot_processes)} running bot instances")
                for process in bot_processes:
                    # Extract PID
                    pid = process.split()[1]
                    logger.info(f"Stopping process {pid}")
                    # Kill the process
                    subprocess.run(f"kill -9 {pid}", shell=True)
                logger.info("All bot instances stopped")
            else:
                logger.info("No running bot instances found")
        else:
            logger.info("No Python processes found")
            
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")
        return False
        
    return True

if __name__ == '__main__':
    logger.info("Starting bot cleanup...")
    if cleanup_bot():
        logger.info("Cleanup completed successfully")
        sys.exit(0)
    else:
        logger.error("Cleanup failed")
        sys.exit(1) 
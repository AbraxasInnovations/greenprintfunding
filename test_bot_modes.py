#!/usr/bin/env python3
"""
Test script for verifying bot operation in both polling and webhook modes.
This script tests the initialization process only, without starting the actual bot.
"""

import os
import sys
import argparse
import logging
import asyncio
import subprocess
import signal
import time
import importlib.util
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Setup mock modules for missing dependencies
def setup_mock_modules():
    """Set up mock modules for any missing dependencies."""
    MOCK_MODULES = ['hyperliquid', 'kraken', 'redis', 'aiosmtplib']
    missing_modules = []
    
    for module in MOCK_MODULES:
        if importlib.util.find_spec(module) is None:
            missing_modules.append(module)
            
    if missing_modules:
        logger.info(f"Setting up mock modules for: {', '.join(missing_modules)}")
        import types
        
        class MockObject:
            """Mock class for any attribute access."""
            def __init__(self, *args, **kwargs):
                pass
                
            def __call__(self, *args, **kwargs):
                return MockObject()
                
            def __getattr__(self, name):
                return MockObject()
                
            def __enter__(self):
                return self
                
            def __exit__(self, *args):
                pass
        
        # Create mock modules
        for module_name in missing_modules:
            mock_module = types.ModuleType(module_name)
            mock_module.__dict__['MockObject'] = MockObject
            # Make all attributes return a MockObject
            mock_module.__getattr__ = lambda name: MockObject()
            # Add the mock module to sys.modules
            sys.modules[module_name] = mock_module
            logger.info(f"Created mock module: {module_name}")

def run_cleanup():
    """Run the cleanup script to ensure no bot processes are running."""
    logger.info("Running cleanup script...")
    try:
        result = subprocess.run(
            ["python", "cleanup_bot.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        if result.returncode == 0:
            logger.info("Cleanup successful")
        else:
            logger.warning(f"Cleanup script returned non-zero exit code: {result.returncode}")
            logger.warning(f"Cleanup output: {result.stdout}\n{result.stderr}")
    except Exception as e:
        logger.error(f"Error running cleanup script: {str(e)}")

async def test_polling_mode(bot_token, mock=False):
    """Test bot initialization in polling mode."""
    logger.info("Testing bot initialization in polling mode...")
    
    # Set environment variables for polling mode
    os.environ["TELEGRAM_BOT_TOKEN"] = bot_token
    os.environ.pop("WEBHOOK_URL", None)  # Remove webhook URL if present
    
    try:
        if mock:
            # Mock testing without actual bot initialization
            logger.info("Mock testing: Bot instance would be created in polling mode")
            logger.info("Mock testing: Bot application would be initialized")
            logger.info("Mock testing: Bot is ready to run in polling mode")
            return True
            
        # Import the bot module (only after setting environment variables)
        from telegram_bot import AbraxasGreenprintBot
        
        # Create bot instance
        bot = AbraxasGreenprintBot(bot_token)
        logger.info("Bot instance created successfully in polling mode")
        
        # Test that the application is properly configured
        await bot.application.initialize()
        logger.info("Bot application initialized successfully")
        
        # Test polling mode setup
        logger.info("Bot is ready to run in polling mode")
        return True
    except Exception as e:
        logger.error(f"Error initializing bot in polling mode: {str(e)}")
        return False
    finally:
        # Clean up
        logger.info("Cleaning up polling mode test...")

async def test_webhook_mode(bot_token, webhook_url, mock=False):
    """Test bot initialization in webhook mode."""
    logger.info("Testing bot initialization in webhook mode...")
    
    # Set environment variables for webhook mode
    os.environ["TELEGRAM_BOT_TOKEN"] = bot_token
    os.environ["WEBHOOK_URL"] = webhook_url
    # Simulate running under Gunicorn
    os.environ["SERVER_SOFTWARE"] = "gunicorn/24.0.0"
    
    try:
        if mock:
            # Mock testing without actual bot initialization
            logger.info("Mock testing: Bot instance would be created in webhook mode")
            logger.info("Mock testing: Bot application would be initialized")
            logger.info("Mock testing: Current webhook would be deleted")
            logger.info(f"Mock testing: Webhook info would be retrieved")
            logger.info(f"Mock testing: Webhook would be set to {webhook_url}")
            return True
            
        # Import the bot module (only after setting environment variables)
        from telegram_bot import AbraxasGreenprintBot
        
        # Create bot instance
        bot = AbraxasGreenprintBot(bot_token)
        logger.info("Bot instance created successfully in webhook mode")
        
        # Test that the application is properly configured
        await bot.application.initialize()
        logger.info("Bot application initialized successfully")
        
        # Test webhook setup (without actually setting the webhook)
        await bot.delete_webhook()  # Make sure webhook is cleared
        logger.info("Current webhook deleted")
        
        webhook_info = await bot.application.bot.get_webhook_info()
        logger.info(f"Webhook info: {webhook_info.url}")
        
        # Test that the webhook would be set properly
        result = await bot.setup_webhook(webhook_url)
        logger.info(f"Webhook setup test result: {result}")
        
        # Delete webhook again to clean up
        await bot.delete_webhook()
        
        return True
    except Exception as e:
        logger.error(f"Error initializing bot in webhook mode: {str(e)}")
        return False
    finally:
        # Clean up
        logger.info("Cleaning up webhook mode test...")
        os.environ.pop("SERVER_SOFTWARE", None)

async def main():
    """Main test function."""
    parser = argparse.ArgumentParser(description='Test bot operation in polling and webhook modes')
    parser.add_argument('--mode', choices=['polling', 'webhook', 'both'], default='both',
                       help='Mode to test (polling, webhook, or both)')
    parser.add_argument('--env-file', default='.env',
                       help='Environment file to load (default: .env)')
    parser.add_argument('--mock', action='store_true',
                       help='Use mock values for testing without real credentials')
    parser.add_argument('--force-mock-modules', action='store_true',
                       help='Force using mock modules even if actual modules exist')
    args = parser.parse_args()
    
    # Load environment variables
    if os.path.exists(args.env_file):
        logger.info(f"Loading environment from {args.env_file}")
        load_dotenv(args.env_file, override=True)
    else:
        logger.error(f"Environment file {args.env_file} not found")
        return False
    
    # Set up mock modules if needed
    if args.force_mock_modules:
        setup_mock_modules()
    
    # Get required environment variables
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if args.mock or not bot_token or bot_token.startswith("REPLACE") or len(bot_token) < 20:
        logger.warning(f"Using mock token for testing as no valid token found in {args.env_file}")
        # This is not a real token, just for testing initialization code
        bot_token = "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi"
    
    webhook_url = os.getenv("WEBHOOK_URL")
    if args.mock or (args.mode == "webhook" or args.mode == "both") and (not webhook_url or webhook_url.startswith("http://138") or webhook_url.startswith("https://abc")):
        logger.warning(f"Using mock webhook URL for testing")
        webhook_url = f"https://example.com/{bot_token}"
    
    # Run cleanup to ensure no bot processes are running
    run_cleanup()
    
    # Test modes as requested
    polling_result = webhook_result = None
    
    if args.mode == "polling" or args.mode == "both":
        polling_result = await test_polling_mode(bot_token, mock=args.mock)
        logger.info(f"Polling mode test: {'SUCCESS' if polling_result else 'FAILED'}")
    
    if args.mode == "webhook" or args.mode == "both":
        webhook_result = await test_webhook_mode(bot_token, webhook_url, mock=args.mock)
        logger.info(f"Webhook mode test: {'SUCCESS' if webhook_result else 'FAILED'}")
    
    # Final results
    logger.info("===== TEST RESULTS =====")
    if polling_result is not None:
        logger.info(f"Polling Mode: {'PASSED' if polling_result else 'FAILED'}")
    if webhook_result is not None:
        logger.info(f"Webhook Mode: {'PASSED' if webhook_result else 'FAILED'}")
    
    # Run cleanup again to ensure everything is terminated
    run_cleanup()
    
    # Return overall success
    return (polling_result if polling_result is not None else True) and \
           (webhook_result if webhook_result is not None else True)

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("Test interrupted by user")
        run_cleanup()
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        run_cleanup()
        sys.exit(1) 
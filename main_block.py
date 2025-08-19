#!/usr/bin/env python3
"""
Main execution block for the Abraxas Greenprint Funding Bot
"""

import os
import sys
import logging
from telegram import Update, error
from telegram.ext import Application, ContextTypes
from aiohttp import web

# This is just a placeholder for the AbraxasGreenprintBot class
class AbraxasGreenprintBot:
    def __init__(self, token):
        self.token = token
        self.application = Application.builder().token(token).build()
        
    async def delete_webhook(self):
        pass
        
    def run(self):
        pass
        
    async def handle_webhook(self, request):
        pass
        
    async def error_handler(self, update, context):
        pass

if __name__ == "__main__":
    # Set up logging first
    logging.basicConfig(
        filename='/opt/crypto-arb-bot/logs/bot.log',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)
    
    try:
        # Create bot instance
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not bot_token:
            logger.error("TELEGRAM_BOT_TOKEN environment variable not set")
            sys.exit(1)
            
        # Create bot instance
        bot = AbraxasGreenprintBot(bot_token)
        logger.info("Bot instance created successfully")
        
        # Register error handler
        bot.application.add_error_handler(bot.error_handler)
        logger.info("Error handler registered")
        
        # Check if running under Gunicorn
        if 'gunicorn' in os.environ.get('SERVER_SOFTWARE', ''):
            # Webhook mode
            webhook_url = os.getenv('WEBHOOK_URL')
            if not webhook_url:
                logger.error("WEBHOOK_URL environment variable not set")
                sys.exit(1)

            try:
                # Set up webhook
                bot.application.bot.set_webhook(webhook_url)
                logger.info(f"Bot started in webhook mode at {webhook_url}")

                # Create web app
                app = web.Application()
                app.router.add_post(f"/{bot_token}", bot.handle_webhook)
                
                # Export for Gunicorn
                web_app = app
            except Exception as e:
                logger.error(f"Failed to set up webhook: {str(e)}", exc_info=True)
                sys.exit(1)
        else:
            # Polling mode
            try:
                logger.info("Bot started in polling mode")
                bot.run()
            except Exception as e:
                logger.error(f"Failed to start polling: {str(e)}", exc_info=True)
                sys.exit(1)

    except Exception as e:
        logger.error(f"Critical error during bot startup: {str(e)}", exc_info=True)
        sys.exit(1) 
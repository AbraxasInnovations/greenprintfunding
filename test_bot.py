#!/usr/bin/env python3
"""
Simple Telegram Bot test script to verify bot token and basic functionality
"""

import os
import logging
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Bot token from environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(f'Hello, {user.first_name}! I am your test bot.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text('This is a test bot to verify functionality.')

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send status information."""
    await update.message.reply_text('Bot is running correctly! Token is valid.')

def main() -> None:
    """Start the bot."""
    # Create the Application instance
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))

    # Log the token being used (first 5 chars for security)
    if TOKEN:
        logger.info(f"Using bot token starting with: {TOKEN[:5]}...")
    else:
        logger.error("No TELEGRAM_BOT_TOKEN found in environment variables!")
        return
    
    # Start the Bot in polling mode
    logger.info("Starting bot in polling mode...")
    application.run_polling()

if __name__ == "__main__":
    main() 
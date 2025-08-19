#!/bin/bash
# Script to restart the Abraxas Greenprint Funding Telegram Bot
# This script only manages the Telegram interface bot, not the trading bot

# Stop any existing Telegram bot processes
if pgrep -f "python.*telegram_bot.py" > /dev/null; then
    echo "Stopping existing Telegram bot processes..."
    pkill -f "python.*telegram_bot.py"
    sleep 2
fi

# Change to the bot directory
cd /opt/crypto-arb-bot

# Activate the virtual environment
source venv/bin/activate

# Start the Telegram bot in the foreground
echo "Starting Telegram bot..."
python3 telegram_bot.py

# Note: This script only manages the Telegram interface bot
# The trading bot (arb_bot.py) is started separately by users through the Telegram interface
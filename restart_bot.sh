#!/bin/bash
# Script to restart the Abraxas Greenprint Funding Bot

# Stop any existing processes
if pgrep -f "python.*telegram_bot.py" > /dev/null; then
    echo "Stopping existing bot processes..."
    pkill -f "python.*telegram_bot.py"
    sleep 2
fi

# Change to the bot directory
cd /opt/crypto-arb-bot

# Activate the virtual environment
source venv/bin/activate

# Remove existing database if needed (only do this for testing!)
# rm -f abraxas_bot.db

# Start the bot in the background
echo "Starting bot..."
nohup python3 telegram_bot.py > logs/startup.log 2>&1 &

# Check if it started
sleep 3
if pgrep -f "python.*telegram_bot.py" > /dev/null; then
    echo "Bot started successfully!"
    echo "Check logs with: tail -f abraxas_bot.log"
else
    echo "Bot failed to start. Check logs for errors."
    cat logs/startup.log
fi
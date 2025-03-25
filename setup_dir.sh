#!/bin/bash
# Setup directories with proper permissions for the Abraxas Greenprint Funding Bot

# Create config directory with proper permissions
mkdir -p /opt/crypto-arb-bot/config
chmod 770 /opt/crypto-arb-bot/config
chown botuser:botuser /opt/crypto-arb-bot/config

# Create logs directory
mkdir -p /opt/crypto-arb-bot/logs
chmod 770 /opt/crypto-arb-bot/logs
chown botuser:botuser /opt/crypto-arb-bot/logs

# Create backups directory
mkdir -p /opt/crypto-arb-bot/backups
chmod 770 /opt/crypto-arb-bot/backups
chown botuser:botuser /opt/crypto-arb-bot/backups

echo "Directories created with proper permissions."
echo "You should now be able to run the bot without permission errors."
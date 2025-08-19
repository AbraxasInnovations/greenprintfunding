# Abraxas Greenprint Funding Bot

A Telegram bot for managing cryptocurrency funding arbitrage trading between Hyperliquid and Kraken exchanges.

## Architecture Overview

The bot uses a unified architecture with a Gunicorn server handling both Telegram updates and payment webhooks. The system is designed with robust error handling and state management to ensure reliable operation.

### Core Components

1. **Webhook Server (`webhook_server.py`)**
   - Handles both Telegram updates and BoomFi payment notifications
   - Verifies webhook signatures
   - Processes payments and updates database
   - Sends notifications to users

2. **Telegram Bot (`telegram_bot.py`)**
   - Manages user interactions
   - Handles subscription management
   - Controls trading operations
   - Provides status updates

3. **Database Layer**
   - Stores user information
   - Manages API keys and wallet addresses
   - Tracks subscriptions and transactions
   - Maintains bot status

### Payment and Subscription Flow

1. **Payment Processing**
   - User initiates payment through BoomFi
   - Webhook server receives payment notification
   - Payment is verified through multiple channels:
     - Direct webhook verification
     - API verification with retries
     - Database status checks

2. **Subscription Activation**
   - After payment verification:
     - Database is updated with subscription details
     - Multiple verification steps ensure consistency
     - User is notified of successful payment
     - System guides user through next steps

3. **Post-Payment Flow**
   - User is guided to token selection
   - After token selection, API key setup begins
   - Once API keys are configured, bot can be started
   - Clear feedback at each stage

4. **Error Handling**
   - Each step has built-in retry mechanisms
   - Database transactions ensure consistency
   - Users receive clear error messages
   - System maintains state through errors

## Features

- Subscription management with tiered access
- Token selection based on subscription tier
- API key management for exchanges
- Trading strategy configuration
- Bot status monitoring and control

## Bot Setup Flow

### 1. Registration
- Users start with `/start` command
- Bot creates user profile in database
- Welcome message with available commands

### 2. Subscription and Payment
- Users select subscription tier with `/subscribe`
- Available tiers:
  - Tier 1: $49/month (1 token)
  - Tier 2: $95/month (2 tokens)
  - Tier 3: $2500/month (All tokens)
- Payment confirmation includes:
  - Tier-specific token limit message
  - "Select Tokens" button for immediate token selection
  - Fallback to `/tokens` command if button fails

### 3. Token Selection
After subscribing, users can select which tokens they want to trade. The number of tokens they can select depends on their subscription tier:
- Tier 1: 1 token
- Tier 2: 2 tokens
- Tier 3: All available tokens

Users can select tokens by:
1. Using the `/tokens` command
2. Clicking the "Select Tokens" button after payment confirmation

The token selection interface will show:
- Available tokens with checkboxes
- Current selections
- Token limit based on subscription tier
- A "Confirm Token Selection" button

After selecting tokens and clicking "Confirm Token Selection", users will receive a confirmation message:
```
✅ Token Selection Confirmed!

Selected Tokens: BTC, ETH
(2/2 tokens selected for Tier 2)

Now, let's configure your trading strategies.
Choose your entry strategy:

### 4. Strategy Configuration
- Entry strategy selection
- Exit strategy selection
- Strategy confirmation
- Integration with token selection flow

### 5. API Key Setup
- Guided setup through `/setkeys` command
- Secure storage of exchange API keys
- Step-by-step process:
  1. Kraken API Key
  2. Kraken API Secret
  3. Hyperliquid API Key
  4. Hyperliquid API Secret
  5. Hyperliquid Wallet Address
- Security warnings and best practices

### 6. Bot Activation
- Start bot with `/start_bot`
- Status monitoring with `/status`
- Stop bot with `/stop_bot`

## Available Commands

- `/start` - Register and begin bot setup
- `/help` - Show help message
- `/pairs` - View available trading pairs
- `/subscribe` - Choose subscription tier
- `/tokens` - Select trading tokens
- `/setkeys` - Configure exchange API keys
- `/status` - Check bot status
- `/start_bot` - Start trading bot
- `/stop_bot` - Stop trading bot
- `/cancel` - Cancel current operation

## Conversation States

The bot uses several conversation states to manage user interactions:

1. `CHOOSING_TIER` - Subscription tier selection
2. `CHOOSING_TOKENS` - Token selection
3. `CHOOSING_ENTRY_STRATEGY` - Entry strategy selection
4. `CHOOSING_EXIT_STRATEGY` - Exit strategy selection
5. `CONFIRMING_STRATEGIES` - Strategy confirmation
6. `CHOOSING_PAYMENT` - Payment method selection
7. `AWAITING_PAYMENT` - Payment processing
8. `AWAITING_KRAKEN_KEY` - Kraken API key input
9. `AWAITING_KRAKEN_SECRET` - Kraken API secret input
10. `AWAITING_HL_KEY` - Hyperliquid API key input
11. `AWAITING_HL_SECRET` - Hyperliquid API secret input
12. `AWAITING_HL_WALLET` - Hyperliquid wallet address input

## Callback Handlers

The bot implements several callback handlers for button interactions:

1. `guide_tokens_callback` - Token selection interface
2. `guide_keys_callback` - API key setup interface
3. `manage_tokens_callback` - Token selection management
4. `entry_strategy_callback` - Entry strategy selection
5. `exit_strategy_callback` - Exit strategy selection
6. `confirm_strategies_callback` - Strategy confirmation
7. `confirm_start_callback` - Bot start confirmation
8. `confirm_stop_callback` - Bot stop confirmation

## Error Handling

The bot includes comprehensive error handling and logging:

1. User validation errors
2. Subscription status checks
3. API key validation
4. Token selection limits
5. Payment processing errors
6. Bot operation errors

All errors are logged with detailed context and appropriate user feedback.

## Security Features

- API key encryption
- Secure message deletion
- User authentication
- Tier-based access control
- Input validation
- Error handling without exposure of sensitive data

## Logging

The bot implements detailed logging for:
- User actions
- System operations
- Error conditions
- Security events
- Bot status changes

Logs are stored in `/opt/crypto-arb-bot/logs/bot.log` with rotation and backup.

### Troubleshooting

#### Common Issues and Solutions

1. **Incorrect Tier Display After Payment**
   - If the bot shows Tier 1 after payment confirmation, try:
     - Using the `/tokens` command directly
     - Waiting a few minutes for the database to update
     - Contacting support if the issue persists

2. **Token Selection Button Not Appearing**
   - If the "Select Tokens" button doesn't appear after payment:
     - Use the `/tokens` command
     - Check your subscription status with `/status`
     - Ensure your payment was confirmed

3. **Token Selection Limits**
   - If you can't select the expected number of tokens:
     - Verify your subscription tier
     - Check your current token selections
     - Use the `/tokens` command to reset selections

4. **Database Synchronization**
   - If you experience delays in updates:
     - Wait a few minutes for the database to sync
     - Try the command again
     - Check the bot's status with `/status`

## Deployment Setup

1. **Install Required Packages**
   ```bash
   pip install gunicorn supervisor python-telegram-bot
   ```

2. **Create Required Directories**
   ```bash
   sudo mkdir -p /opt/crypto-arb-bot/logs
   sudo chown -R $USER:$USER /opt/crypto-arb-bot
   ```

3. **Configure Environment Variables**
   Create `.env` file with:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token
   WEBHOOK_URL=https://your-domain.com/webhook
   WEBHOOK_PORT=8443
   BOOMFI_API_KEY=your_boomfi_key
   ENCRYPTION_MASTER_KEY=your_encryption_key
   ```

4. **Set Up Supervisor**
   Create `/etc/supervisor/conf.d/crypto-arb-bot.conf`:
   ```ini
   [program:crypto-arb-bot]
   command=gunicorn webhook_server:app -b 0.0.0.0:8443
   directory=/opt/crypto-arb-bot
   user=your_user
   autostart=true
   autorestart=true
   stderr_logfile=/opt/crypto-arb-bot/logs/bot_error.log
   stdout_logfile=/opt/crypto-arb-bot/logs/bot.log
   environment=PYTHONPATH="/opt/crypto-arb-bot"
   ```

5. **Start the Service**
   ```bash
   sudo supervisorctl reread
   sudo supervisorctl update
   sudo supervisorctl start crypto-arb-bot
   ```

## Monitoring and Maintenance

1. **Check Service Status**
   ```bash
   sudo supervisorctl status crypto-arb-bot
   ```

2. **View Logs**
   ```bash
   tail -f /opt/crypto-arb-bot/logs/bot.log
   tail -f /opt/crypto-arb-bot/logs/bot_error.log
   ```

3. **Restart Service**
   ```bash
   sudo supervisorctl restart crypto-arb-bot
   ```

## Development Mode

For testing, run the bot in polling mode:
```bash
python3 telegram_bot.py
```

## Troubleshooting

1. **Webhook Issues**
   - Check webhook URL configuration
   - Verify SSL certificate
   - Monitor webhook logs

2. **Payment Processing**
   - Check BoomFi API key
   - Verify webhook signatures
   - Monitor payment status in database

3. **Bot Operation**
   - Check API key configuration
   - Verify exchange connectivity
   - Monitor trading logs

4. **Database Issues**
   - Check database connection
   - Verify data consistency
   - Monitor transaction logs

## Deployment

### Prerequisites

- Python 3.8+
- systemd-based Linux system
- Domain name with SSL certificate (for webhook mode)
- PostgreSQL database
- Supervisor (for process management)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/crypto-arb-bot.git
cd crypto-arb-bot
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Create environment file:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Setup the service:
```bash
sudo ./manage.sh setup
```

5. Install and configure Supervisor:
```bash
sudo apt-get install supervisor
sudo cp crypto-arb-bot.conf /etc/supervisor/conf.d/
sudo supervisorctl reread
sudo supervisorctl update
```

### Management

The bot can be managed either through the management script or Supervisor:

#### Using manage.sh
```bash
./manage.sh start   # Start the service
./manage.sh logs    # View logs
```

#### Using Supervisor
    ```bash
sudo supervisorctl status crypto-arb-bot    # Check status
sudo supervisorctl start crypto-arb-bot     # Start service
sudo supervisorctl stop crypto-arb-bot      # Stop service
sudo supervisorctl restart crypto-arb-bot   # Restart service
```

### Logging

Comprehensive logging is implemented across the application:

- Bot operations: /opt/crypto-arb-bot/logs/bot.log
- Gunicorn access: /opt/crypto-arb-bot/logs/gunicorn_access.log
- Gunicorn errors: /opt/crypto-arb-bot/logs/gunicorn_error.log
- Supervisor stdout: /opt/crypto-arb-bot/logs/supervisor_stdout.log
- Supervisor stderr: /opt/crypto-arb-bot/logs/supervisor_stderr.log

Log levels and formats can be configured in the respective configuration files. 
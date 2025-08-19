#!/bin/bash
# Abraxas Greenprint Funding Bot - Setup Script
# This script sets up the bot environment on your Digital Ocean droplet

# Exit on any error
set -e

# Check if script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (use sudo)"
  exit 1
fi

echo "============================================"
echo "  Abraxas Greenprint Funding Bot Setup"
echo "============================================"
echo ""

# Update system packages
echo "Updating system packages..."
apt update && apt upgrade -y

# Install required system dependencies
echo "Installing system dependencies..."
apt install -y python3 python3-pip python3-venv git sqlite3 supervisor nginx

# Create bot user
echo "Creating dedicated user for the bot..."
if id "botuser" &>/dev/null; then
    echo "User 'botuser' already exists"
else
    adduser --gecos "" botuser
    usermod -aG sudo botuser
fi

# Create project directory
echo "Creating project directory..."
mkdir -p /opt/abraxas-bot
mkdir -p /opt/abraxas-bot/logs
mkdir -p /opt/abraxas-bot/config
chown -R botuser:botuser /opt/abraxas-bot

# Switch to bot user for next steps
echo "Setting up the Python environment..."
su - botuser << 'EOF'
cd /opt/abraxas-bot

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required Python packages
pip install python-telegram-bot sqlalchemy cryptography requests websocket-client numpy pandas pytz eth-account python-dotenv
pip install hyperliquid-python-sdk
# Add packages for Paddle integration and webhook server
pip install flask gunicorn pycryptodome requests-toolbelt
EOF

# Create environment file
echo "Creating environment file template..."
cat > /opt/abraxas-bot/.env.example << EOF
# Telegram Bot Token (Get from @BotFather)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# Database Configuration
DATABASE_URL=sqlite:///abraxas_bot.db

# Encryption Master Key (Generate using command below)
# python3 -c "import os; import base64; print(base64.urlsafe_b64encode(os.urandom(32)).decode())"
ENCRYPTION_MASTER_KEY=

# Payment Wallet Addresses (Legacy)
BTC_PAYMENT_ADDRESS=your_btc_address
SOL_PAYMENT_ADDRESS=your_sol_address
USDC_PAYMENT_ADDRESS=your_usdc_address

# Blockchain API Keys (Optional but recommended)
BLOCKCYPHER_TOKEN=
SOLANA_API_KEY=

# Paddle Payment Integration
PADDLE_VENDOR_ID=your_paddle_vendor_id
PADDLE_API_KEY=your_paddle_api_key
PADDLE_PUBLIC_KEY=your_paddle_public_key
PADDLE_WEBHOOK_SECRET=your_paddle_webhook_secret
PADDLE_PRODUCT_TIER1=product_id_for_tier1
PADDLE_PRODUCT_TIER2=product_id_for_tier2
PADDLE_PRODUCT_TIER3=product_id_for_tier3
PADDLE_TEST_MODE=true
WEBHOOK_URL=https://your-domain.com/webhook/paddle

# For local testing only (set to false in production)
AUTO_APPROVE_PAYMENTS=false
EOF

# Copy to actual .env file that user will populate
cp /opt/abraxas-bot/.env.example /opt/abraxas-bot/.env
chown botuser:botuser /opt/abraxas-bot/.env
chmod 600 /opt/abraxas-bot/.env

# Set up supervisor configuration
echo "Setting up supervisor to manage the bot..."
cat > /etc/supervisor/conf.d/abraxas-bot.conf << EOF
[program:abraxas-bot]
command=/opt/abraxas-bot/venv/bin/python /opt/abraxas-bot/telegram_bot.py
directory=/opt/abraxas-bot
user=botuser
autostart=true
autorestart=true
startretries=10
stopwaitsecs=30
stdout_logfile=/opt/abraxas-bot/logs/bot.log
stderr_logfile=/opt/abraxas-bot/logs/bot_error.log
environment=PYTHONUNBUFFERED=1
EOF

# Set up webhook server configuration
cat > /etc/supervisor/conf.d/webhook-server.conf << EOF
[program:webhook-server]
command=/opt/abraxas-bot/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 webhook_server:app
directory=/opt/abraxas-bot
user=botuser
autostart=true
autorestart=true
startretries=10
stopwaitsecs=30
stdout_logfile=/opt/abraxas-bot/logs/webhook.log
stderr_logfile=/opt/abraxas-bot/logs/webhook_error.log
environment=PYTHONUNBUFFERED=1
EOF

# Setup nginx as a reverse proxy for the webhook server
echo "Setting up Nginx reverse proxy for webhook server..."
cat > /etc/nginx/sites-available/webhook << 'EOF'
server {
    listen 80;
    server_name your-domain.com;  # Replace with your actual domain

    location /webhook/ {
        proxy_pass http://127.0.0.1:5000/webhook/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF
ln -sf /etc/nginx/sites-available/webhook /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

# Create a script to easily check logs
cat > /opt/abraxas-bot/check_logs.sh << 'EOF'
#!/bin/bash
echo "Bot logs:"
tail -f /opt/abraxas-bot/logs/bot.log
EOF

cat > /opt/abraxas-bot/check_webhook_logs.sh << 'EOF'
#!/bin/bash
echo "Webhook logs:"
tail -f /opt/abraxas-bot/logs/webhook.log
EOF

chmod +x /opt/abraxas-bot/check_logs.sh
chmod +x /opt/abraxas-bot/check_webhook_logs.sh
chown botuser:botuser /opt/abraxas-bot/check_logs.sh
chown botuser:botuser /opt/abraxas-bot/check_webhook_logs.sh

# Create a script to generate backup files
mkdir -p /opt/abraxas-bot/backups
cat > /opt/abraxas-bot/backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y-%m-%d)
mkdir -p /opt/abraxas-bot/backups
cp /opt/abraxas-bot/abraxas_bot.db /opt/abraxas-bot/backups/abraxas_bot_$DATE.db
echo "Backup created: /opt/abraxas-bot/backups/abraxas_bot_$DATE.db"
EOF
chmod +x /opt/abraxas-bot/backup.sh
chown botuser:botuser /opt/abraxas-bot/backup.sh

# Set up daily backups
echo "0 0 * * * /opt/abraxas-bot/backup.sh" | crontab -u botuser -

echo ""
echo "============================================"
echo "Setup completed! Next steps:"
echo "============================================"
echo "1. Copy your Python files to /opt/abraxas-bot/"
echo "2. Edit /opt/abraxas-bot/.env to add your configuration"
echo "3. Update 'your-domain.com' in /etc/nginx/sites-available/webhook with your actual domain"
echo "4. Obtain SSL certificate (recommended): sudo certbot --nginx -d your-domain.com"
echo "5. Start services: sudo supervisorctl reread && sudo supervisorctl update"
echo "6. Start the bot with: sudo supervisorctl start abraxas-bot webhook-server"
echo "7. Check logs with: /opt/abraxas-bot/check_logs.sh or /opt/abraxas-bot/check_webhook_logs.sh"
echo ""
echo "Don't forget to set up your Paddle account and configure the webhook"
echo "See PADDLE_SETUP.md for detailed instructions"
echo "============================================"
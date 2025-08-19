#!/bin/bash

set -e

# Configuration
SERVICE_NAME="crypto-arb-bot"
INSTALL_DIR="/opt/crypto-arb-bot"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
LOG_DIR="${INSTALL_DIR}/logs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}This script must be run as root${NC}"
   exit 1
fi

# Create required directories
setup_directories() {
    mkdir -p ${INSTALL_DIR}
    mkdir -p ${LOG_DIR}
    chown -R www-data:www-data ${INSTALL_DIR}
    chmod 755 ${INSTALL_DIR}
}

# Install service file
setup_service() {
    cp crypto-arb-bot.service ${SERVICE_FILE}
    systemctl daemon-reload
    systemctl enable ${SERVICE_NAME}
    echo -e "${GREEN}Service installed successfully${NC}"
}

# Initial setup
setup() {
    echo "Setting up ${SERVICE_NAME}..."
    setup_directories
    setup_service
    echo "Setup complete. Edit .env file and start the service."
}

# Start the service
start() {
    echo "Starting ${SERVICE_NAME}..."
    systemctl start ${SERVICE_NAME}
    echo -e "${GREEN}Service started${NC}"
}

# Stop the service
stop() {
    echo "Stopping ${SERVICE_NAME}..."
    systemctl stop ${SERVICE_NAME}
    echo -e "${YELLOW}Service stopped${NC}"
}

# Restart the service
restart() {
    echo "Restarting ${SERVICE_NAME}..."
    systemctl restart ${SERVICE_NAME}
    echo -e "${GREEN}Service restarted${NC}"
}

# Check service status
status() {
    systemctl status ${SERVICE_NAME}
}

# View logs
logs() {
    if [ "$2" == "gunicorn" ]; then
        tail -f ${LOG_DIR}/gunicorn_*.log
    else
        tail -f ${LOG_DIR}/bot.log
    fi
}

# Command processing
case "$1" in
    setup)
        setup
        ;;
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    logs)
        logs "$@"
        ;;
    *)
        echo "Usage: $0 {setup|start|stop|restart|status|logs}"
        exit 1
        ;;
esac

exit 0 
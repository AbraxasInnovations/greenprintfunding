import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2
# Add max requests to prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = '/opt/crypto-arb-bot/logs/gunicorn_access.log'
errorlog = '/opt/crypto-arb-bot/logs/gunicorn_error.log'
loglevel = 'info'
# Capture output from the application
capture_output = True

# Process naming
proc_name = 'crypto_arb_bot'

# SSL (if needed)
# keyfile = '/path/to/your/ssl/key.pem'
# certfile = '/path/to/your/ssl/cert.pem'

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Server Mechanics
graceful_timeout = 30
# Reuse port for faster restarts
reuse_port = True
# Set a temporary directory for worker heartbeats (if needed)
# worker_tmp_dir = '/opt/crypto-arb-bot/worker_tmp' 
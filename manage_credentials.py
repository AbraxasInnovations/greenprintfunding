#!/usr/bin/env python3
"""
Credential management script for testing the crypto arbitrage bot.
This script handles secure storage and retrieval of test API credentials.
"""

import os
import json
import sys
import getpass
from cryptography.fernet import Fernet

# Configuration
KEY_FILE = '.test_key'
CREDENTIALS_FILE = '.test_credentials'

def get_key():
    """Generate or load encryption key."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as f:
            return f.read()
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(key)
    print(f"Generated new encryption key and saved to {KEY_FILE}")
    return key

def store_test_credentials():
    """Store API keys securely for testing."""
    credentials = {
        'kraken': {
            'api_key': getpass.getpass('Enter test Kraken API key: '),
            'api_secret': getpass.getpass('Enter test Kraken API secret: ')
        },
        'hyperliquid': {
            'api_key': getpass.getpass('Enter test Hyperliquid API key: '),
            'api_secret': getpass.getpass('Enter test Hyperliquid API secret: '),
            'wallet': getpass.getpass('Enter test Hyperliquid wallet: ')
        }
    }
    
    # Encrypt credentials
    cipher = Fernet(get_key())
    encrypted = cipher.encrypt(json.dumps(credentials).encode())
    
    with open(CREDENTIALS_FILE, 'wb') as f:
        f.write(encrypted)
    print(f"Test credentials stored successfully in {CREDENTIALS_FILE}")

def get_test_credentials():
    """Retrieve API keys for testing."""
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"No test credentials found in {CREDENTIALS_FILE}. Please run 'store' command first.")
        return None
        
    cipher = Fernet(get_key())
    try:
        with open(CREDENTIALS_FILE, 'rb') as f:
            encrypted = f.read()
        
        decrypted = cipher.decrypt(encrypted)
        return json.loads(decrypted.decode())
    except Exception as e:
        print(f"Error retrieving credentials: {str(e)}")
        return None

def inject_credentials_to_env():
    """Inject credentials into environment variables for testing."""
    credentials = get_test_credentials()
    if not credentials:
        return False
    
    # Set Kraken credentials
    if 'kraken' in credentials:
        os.environ['KRAKEN_API_KEY'] = credentials['kraken']['api_key']
        os.environ['KRAKEN_API_SECRET'] = credentials['kraken']['api_secret']
        print("Injected Kraken credentials into environment variables")
    
    # Set Hyperliquid credentials
    if 'hyperliquid' in credentials:
        os.environ['HYPERLIQUID_API_KEY'] = credentials['hyperliquid']['api_key']
        os.environ['HYPERLIQUID_API_SECRET'] = credentials['hyperliquid']['api_secret']
        os.environ['HYPERLIQUID_WALLET'] = credentials['hyperliquid']['wallet']
        print("Injected Hyperliquid credentials into environment variables")
    
    return True

def list_credentials():
    """List available credentials (without showing values)."""
    credentials = get_test_credentials()
    if not credentials:
        return
    
    print("\nAvailable test credentials:")
    print("--------------------------")
    
    for exchange, creds in credentials.items():
        print(f"\n{exchange.upper()}:")
        for key, value in creds.items():
            # Show only first few characters of each credential
            masked_value = value[:4] + "*" * (len(value) - 4) if value else "(empty)"
            print(f"  {key}: {masked_value}")

def clear_credentials():
    """Clear all stored credentials."""
    if os.path.exists(CREDENTIALS_FILE):
        os.unlink(CREDENTIALS_FILE)
        print(f"Credentials file {CREDENTIALS_FILE} deleted")
    if os.path.exists(KEY_FILE):
        os.unlink(KEY_FILE)
        print(f"Key file {KEY_FILE} deleted")
    print("All credentials cleared")

def show_help():
    """Show help message."""
    print(f"\nUsage: {sys.argv[0]} COMMAND\n")
    print("Commands:")
    print("  store      Store new test credentials")
    print("  get        Retrieve and display stored credentials")
    print("  list       List available credentials (masked)")
    print("  inject     Inject credentials into environment variables")
    print("  clear      Clear all stored credentials")
    print("  help       Show this help message")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
        
    command = sys.argv[1].lower()
    
    if command == 'store':
        store_test_credentials()
    elif command == 'get':
        creds = get_test_credentials()
        if creds:
            print(json.dumps(creds, indent=2))
    elif command == 'list':
        list_credentials()
    elif command == 'inject':
        inject_credentials_to_env()
    elif command == 'clear':
        clear_credentials()
    elif command in ['help', '-h', '--help']:
        show_help()
    else:
        print(f"Unknown command: {command}")
        show_help()
        sys.exit(1) 
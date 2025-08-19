#!/usr/bin/env python3
"""
Test script to derive an Ethereum wallet address from a private key
using the eth_account library.
"""

from eth_account import Account
import secrets # Used to generate a dummy key if needed

# --- IMPORTANT ---
# Replace this placeholder with a valid 64-character hex private key string (without '0x' prefix)
# For testing, DO NOT use your real Hyperliquid private key here unless you are sure about your environment.
# You can generate a temporary one or use a known test key.
# Example format: 'aabbccddeeff00112233445566778899aabbccddeeff00112233445566778899'

# Option 1: Use a placeholder (script will fail until replaced)
private_key_hex = "7a7191d8cc249a376aa1c547c86c7f46d0bf909e116452272dc67760fc86a951"

# Option 2: Generate a random dummy private key for testing (RECOMMENDED for quick test)
#private_key_bytes = secrets.token_bytes(32)
#private_key_hex = private_key_bytes.hex()
#print(f"Generated Dummy Private Key: {private_key_hex}\n") # Print the key used for the test

# --- End of Section to Modify ---

# Ensure the key is 64 hex characters
if len(private_key_hex) != 64:
    print(f"Error: Private key must be 64 hexadecimal characters long (found {len(private_key_hex)}).")
    print("Please ensure the key does not have the '0x' prefix.")
    exit(1)

try:
    # Derive the account object from the private key
    account = Account.from_key(private_key_hex)

    # Get the wallet address
    wallet_address = account.address

    print(f"Private Key Used: {private_key_hex[:4]}...{private_key_hex[-4:]}")
    print(f"Derived Wallet Address: {wallet_address}")

except ValueError as e:
    print(f"Error: Invalid private key format.")
    print(f"Details: {e}")
    exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit(1) 
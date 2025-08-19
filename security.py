#!/usr/bin/env python3
"""
Security Module for the Crypto Arbitrage Bot
-------------------------------------------
Handles encryption and security related functions
"""

import os
import base64
from typing import Tuple, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

class SecurityManager:
    """Manages encryption and security functions"""
    
    def __init__(self):
        # Get master key from environment or generate one
        self.master_key = os.getenv('ENCRYPTION_MASTER_KEY')
        if not self.master_key:
            logger.warning("ENCRYPTION_MASTER_KEY not found in environment, generating a new one")
            self.master_key = Fernet.generate_key().decode()
            logger.warning(f"Generated master key: {self.master_key}")
            logger.warning("Add this to your .env file as ENCRYPTION_MASTER_KEY")
        
        # Convert string key to bytes if needed
        if isinstance(self.master_key, str):
            self.master_key = self.master_key.encode()
            
    def generate_key(self, salt: bytes) -> bytes:
        """Generate a Fernet key from master key and salt"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.master_key))
        return key
    
    def encrypt(self, data: str) -> Tuple[bytes, bytes]:
        """
        Encrypt data using Fernet symmetric encryption
        
        Args:
            data: String data to encrypt
            
        Returns:
            Tuple of (encrypted_data, initialization_vector)
        """
        try:
            # Generate a random salt/IV for this encryption
            salt = os.urandom(16)
            
            # Create a key using the salt
            key = self.generate_key(salt)
            
            # Create a Fernet cipher with the derived key
            cipher = Fernet(key)
            
            # Encrypt the data
            encrypted_data = cipher.encrypt(data.encode())
            
            return encrypted_data, salt
        except Exception as e:
            logger.error(f"Encryption error: {str(e)}")
            raise
    
    def decrypt(self, encrypted_data: bytes, salt: bytes) -> str:
        """
        Decrypt data using Fernet symmetric encryption
        
        Args:
            encrypted_data: Encrypted data bytes
            salt: Salt/IV used during encryption
            
        Returns:
            Decrypted string
        """
        try:
            # Recreate the key using the provided salt
            key = self.generate_key(salt)
            
            # Create a Fernet cipher with the derived key
            cipher = Fernet(key)
            
            # Decrypt the data
            decrypted_data = cipher.decrypt(encrypted_data)
            
            return decrypted_data.decode()
        except Exception as e:
            logger.error(f"Decryption error: {str(e)}")
            raise
    
    def validate_api_key(self, key: str, exchange: str) -> bool:
        """
        Validate API key format
        
        Args:
            key: API key to validate
            exchange: Exchange name (kraken, hyperliquid)
            
        Returns:
            True if valid, False otherwise
        """
        if not key or not isinstance(key, str):
            return False
            
        # Kraken API key validation
        if exchange.lower() == 'kraken':
            # Kraken keys are typically 56 characters
            return len(key) >= 40 and len(key) <= 80
            
        # Hyperliquid validation
        elif exchange.lower() == 'hyperliquid':
            # Keys usually start with 0x and are 64 hex characters
            if key.startswith('0x') and len(key) == 66:
                return True
            # Or just 64 hex characters
            if len(key) == 64 and all(c in '0123456789abcdefABCDEF' for c in key):
                return True
            return False
            
        return True  # Default to true for unknown exchanges
        
    def validate_private_key(self, key: str) -> bool:
        """
        Validate Ethereum private key format
        
        Args:
            key: Private key to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not key or not isinstance(key, str):
            return False
            
        # Remove 0x prefix if present
        if key.startswith('0x'):
            key = key[2:]
            
        # Check if it's 64 hex characters
        if len(key) != 64:
            return False
            
        # Check if all characters are hex
        try:
            int(key, 16)
            return True
        except ValueError:
            return False
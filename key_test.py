#!/usr/bin/env python3
"""Test script to verify RSA public key loading"""

import os
from dotenv import load_dotenv
load_dotenv()

try:
    from Crypto.PublicKey import RSA
    key = os.getenv('BOOMFI_WEBHOOK_PUBLIC_KEY')
    print(f'Key length: {len(key) if key else 0}')
    print(f'Key preview: {key[:30]}...' if key else 'None')
    
    formatted_key = f'-----BEGIN PUBLIC KEY-----\n{key}\n-----END PUBLIC KEY-----' if key and '-----BEGIN PUBLIC KEY-----' not in key else key
    print(f'Formatted key length: {len(formatted_key) if formatted_key else 0}')
    
    try:
        rsa_key = RSA.importKey(formatted_key)
        print('✅ Public key loaded successfully.')
    except Exception as e:
        print(f'❌ Failed to import formatted key: {e}')
        
    # Try loading the raw key directly
    if key:
        try:
            raw_rsa_key = RSA.importKey(key)
            print('✅ Raw public key loaded successfully.')
        except Exception as e:
            print(f'❌ Failed to import raw key: {e}')
    else:
        print('❌ No key found in environment variables')
        
except ImportError:
    print('❌ pycryptodome not installed. Install with: pip install pycryptodome') 
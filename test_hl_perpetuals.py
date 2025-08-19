#!/usr/bin/env python3
"""
Test script for fetching Hyperliquid perpetual pairs
Uses the meta endpoint to get available tokens without authentication
"""

import requests
import json
from typing import List, Dict
from trading_pairs import AVAILABLE_PAIRS

def get_all_hyperliquid_perps() -> List[str]:
    """Get list of all available perpetual pairs on Hyperliquid"""
    api_url = "https://api.hyperliquid.xyz/info"
    
    try:
        payload = {"type": "meta"}
        response = requests.post(api_url, json=payload)
        meta_data = response.json()
        
        # Extract token names
        tokens = [coin['name'] for coin in meta_data['universe']]
        return tokens
    except Exception as e:
        print(f"Error getting token list: {e}")
        return []

def check_tokens_availability(hl_tokens: List[str]) -> Dict[str, bool]:
    """Check which tokens from our configuration are available on Hyperliquid"""
    results = {}
    
    for token in AVAILABLE_PAIRS.keys():
        available = token in hl_tokens
        results[token] = available
    
    return results

def main():
    print("Fetching list of all Hyperliquid perpetual pairs...")
    tokens = get_all_hyperliquid_perps()
    
    if not tokens:
        print("Failed to get token list.")
        return
    
    print(f"\nFound {len(tokens)} perpetual pairs on Hyperliquid.")
    print("First 10 tokens as sample:", tokens[:10])
    
    # Check which tokens from our configuration are available
    print("\nChecking our tokens against Hyperliquid availability:")
    availability = check_tokens_availability(tokens)
    
    # Group tokens by availability
    available = [token for token, is_available in availability.items() if is_available]
    not_available = [token for token, is_available in availability.items() if not is_available]
    
    print(f"\nOur tokens available on Hyperliquid ({len(available)}):")
    for i, token in enumerate(sorted(available)):
        print(f"{token}", end=", " if (i+1) % 10 != 0 else "\n")
    
    print(f"\n\nOur tokens NOT available on Hyperliquid ({len(not_available)}):")
    for i, token in enumerate(sorted(not_available)):
        print(f"{token}", end=", " if (i+1) % 10 != 0 else "\n")
    
    # Check if BADGER and ETH are available
    print("\nSpecific token availability:")
    for special_token in ["BADGER", "ETH", "BTC", "HPOS"]:
        print(f"{special_token}: {'Available' if special_token in tokens else 'Not available'}")
    
    # Print the full raw response for debugging
    print("\nWould you like to see the full API response? (y/n)")
    choice = input()
    if choice.lower() == 'y':
        payload = {"type": "meta"}
        response = requests.post("https://api.hyperliquid.xyz/info", json=payload)
        print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    main() 
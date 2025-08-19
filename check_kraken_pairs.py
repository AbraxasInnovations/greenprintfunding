#!/usr/bin/env python3
"""
Kraken Pair Name Verification Script
-----------------------------------
This script fetches all available trading pairs from Kraken API
and compares them with the pairs defined in trading_pairs.py
"""

import requests
import json
import sys
from trading_pairs import AVAILABLE_PAIRS

def get_kraken_pairs():
    """Fetch all trading pairs from Kraken API"""
    url = "https://api.kraken.com/0/public/AssetPairs"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "result" in data:
                return data["result"]
        print(f"Error fetching pairs: {response.status_code}")
        return {}
    except Exception as e:
        print(f"Exception: {str(e)}")
        return {}

def main():
    # Get pairs from Kraken API
    kraken_pairs = get_kraken_pairs()
    
    # Only include USD pairs for simplicity
    usd_pairs = {pair: details for pair, details in kraken_pairs.items() 
                if pair.endswith('USD') or pair.endswith('ZUSD')}
    
    # Get pairs from our config
    our_pairs = {pair: config["kraken_pair"] for pair, config in AVAILABLE_PAIRS.items() 
                if config["kraken_pair"] is not None}
    
    # Find mismatches
    mismatches = []
    missing_pairs = []
    
    for token, pair_name in our_pairs.items():
        if pair_name not in kraken_pairs:
            # Try alternate endings
            alternates = []
            if pair_name.endswith('USD'):
                alternates.append(pair_name.replace('USD', 'ZUSD'))
            elif pair_name.endswith('ZUSD'):
                alternates.append(pair_name.replace('ZUSD', 'USD'))
            
            found = False
            for alt in alternates:
                if alt in kraken_pairs:
                    mismatches.append((token, pair_name, alt))
                    found = True
                    break
            
            if not found:
                missing_pairs.append((token, pair_name))
    
    # Print results
    print("KRAKEN PAIRS VERIFICATION REPORT")
    print("===============================\n")
    
    print(f"Total Kraken USD pairs: {len(usd_pairs)}")
    print(f"Total pairs in our config: {len(our_pairs)}")
    
    print("\nPOTENTIAL MISMATCHES (our config vs. actual Kraken):")
    if mismatches:
        for token, our_name, actual_name in mismatches:
            print(f"  {token}: {our_name} -> should be {actual_name}")
    else:
        print("  None found")
    
    print("\nMISSING PAIRS (not found in Kraken API):")
    if missing_pairs:
        for token, pair_name in missing_pairs:
            print(f"  {token}: {pair_name}")
    else:
        print("  None found")
    
    print("\nALL AVAILABLE KRAKEN USD PAIRS:")
    for pair in sorted(usd_pairs.keys()):
        print(f"  {pair}")

if __name__ == "__main__":
    main() 
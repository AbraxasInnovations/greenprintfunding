import requests
import json
from collections import deque

def get_kraken_asset_pairs():
    """
    Get asset pair information from Kraken API
    """
    url = "https://api.kraken.com/0/public/AssetPairs"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("result", {})
    else:
        print(f"Error fetching Kraken asset pairs: {response.status_code}")
        return {}

def get_hyperliquid_markets():
    """
    Get market information from Hyperliquid API for perpetual futures
    """
    # Direct endpoint to get all perpetual futures on Hyperliquid
    url = "https://api.hyperliquid.xyz/info"
    payload = {"type": "allMids"}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching Hyperliquid markets: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Exception when fetching Hyperliquid markets: {str(e)}")
        return {}

def create_token_dictionary():
    """
    Create a dictionary of tokens with all required fields, only including
    tokens that are available on both Hyperliquid (perp) and Kraken (spot)
    """
    # Get data from APIs
    kraken_pairs = get_kraken_asset_pairs()
    hyperliquid_data = get_hyperliquid_markets()
    
    # Debug: Print the raw responses to understand the structure
    print("Hyperliquid response structure:")
    print(json.dumps(hyperliquid_data, indent=2)[:500] + "..." if hyperliquid_data else "Empty response")
    
    # Try a different approach for Hyperliquid
    if not hyperliquid_data:
        print("Trying alternative Hyperliquid API endpoint...")
        url = "https://api.hyperliquid.xyz/info"
        payload = {"type": "universe"}
        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                hyperliquid_data = response.json()
                print("Alternative endpoint response:")
                print(json.dumps(hyperliquid_data, indent=2)[:500] + "..." if hyperliquid_data else "Empty response")
            else:
                print(f"Error with alternative endpoint: {response.status_code}")
        except Exception as e:
            print(f"Exception with alternative endpoint: {str(e)}")
    
    # Process Hyperliquid data to get coin list
    hl_coins = set()
    
    # Try different structures that might exist in the response
    # Method 1: Check for assetCtxs structure
    if isinstance(hyperliquid_data, dict) and "assetCtxs" in hyperliquid_data:
        for asset in hyperliquid_data["assetCtxs"]:
            if "name" in asset:
                hl_coins.add(asset["name"])
    
    # Method 2: Check for array of coin names
    elif isinstance(hyperliquid_data, list):
        for item in hyperliquid_data:
            if isinstance(item, str):  # Direct coin name
                hl_coins.add(item)
            elif isinstance(item, dict) and "coin" in item:  # Object with coin property
                hl_coins.add(item["coin"])
    
    # Method 3: Check for object with coin keys
    elif isinstance(hyperliquid_data, dict):
        for key in hyperliquid_data.keys():
            hl_coins.add(key)
    
    print(f"Found {len(hl_coins)} coins on Hyperliquid: {sorted(list(hl_coins))[:10]}...")
    
    # Create a mapping of coin symbols to their Kraken pair names
    kraken_coins = set()
    kraken_pair_mapping = {}
    
    for pair_name, pair_data in kraken_pairs.items():
        # Extract base asset (e.g., BTC from XXBTZUSD)
        base_asset = pair_data.get("base", "")
        
        # Only include USD pairs
        if pair_data.get("quote", "") in ["ZUSD", "USD"]:
            # Clean the symbol for comparison
            clean_base = base_asset.replace("X", "").replace("Z", "")
            kraken_coins.add(clean_base)
            kraken_pair_mapping[clean_base] = pair_name
    
    print(f"Found {len(kraken_coins)} coins on Kraken: {sorted(list(kraken_coins))[:10]}...")
    
    # Manual mapping for common naming differences
    mapping_hl_to_kraken = {
        "BTC": "XBT",  # Bitcoin is XBT on Kraken
        "DOGE": "XDG",  # Dogecoin mapping
        # Add more mappings as needed
    }
    
    # Find the intersection - coins available on both platforms
    common_coins = set()
    
    # Check direct matches
    common_coins = hl_coins.intersection(kraken_coins)
    
    # Check matches with manual mapping
    for hl_coin in hl_coins:
        kraken_equivalent = mapping_hl_to_kraken.get(hl_coin)
        if kraken_equivalent and kraken_equivalent in kraken_coins:
            common_coins.add(hl_coin)
    
    print(f"Found {len(common_coins)} coins common to both exchanges: {sorted(list(common_coins))}")
    
    # Add special cases with known mappings
    special_cases = {
        "HPOS": "HPOS10I"  # Special case for Harry Potter
    }
    
    for hl_name, kraken_name in special_cases.items():
        if hl_name in hl_coins and kraken_name in kraken_coins:
            common_coins.add(hl_name)
    
    # Now create entries for each common coin
    tokens = {}
    for coin in common_coins:
        # Get the Kraken pair name
        kraken_equiv = mapping_hl_to_kraken.get(coin, coin)
        special_equiv = special_cases.get(coin)
        
        if special_equiv and special_equiv in kraken_pair_mapping:
            kraken_pair = kraken_pair_mapping[special_equiv]
        elif kraken_equiv in kraken_pair_mapping:
            kraken_pair = kraken_pair_mapping[kraken_equiv]
        else:
            kraken_pair = None
        
        # Determine price precision based on available data
        price_precision = 4  # Default precision
        
        # Special cases:
        if coin == "BTC":
            price_precision = 1
        elif coin in ["ETH", "HPOS"]:
            price_precision = 2
        elif coin == "DOGE":
            price_precision = 6
        
        # Default order type is "limit" except for HPOS
        hl_order_type = "market" if coin == "HPOS" else "limit"
        
        # Create the token entry
        tokens[coin] = {
            "position_size": 12.0,  # Total position size in USD
            "margin_size": 4.0,  # Approximate margin required
            "hl_order_type": hl_order_type,  # Order type on Hyperliquid
            "percentile_threshold": 60,  # Entry threshold percentile
            "websocket_subscribed": False,  # Track subscription status per asset
            "in_position": False,  # Track position status per asset
            "hl_position_size": 0.0,  # Current HL position size
            "kraken_position_size": 0.0,  # Current Kraken position size
            "historical_rates": "deque(maxlen=500)",  # Historical funding rates as string
            "percentile_60": None,  # 60th percentile threshold
            "current_hl_order_id": None,  # Current HL order ID
            "current_kraken_order_id": None,  # Current Kraken order ID
            "hl_best_bid": None,  # Current HL best bid
            "hl_best_ask": None,  # Current HL best ask
            "kraken_best_bid": None,  # Current Kraken best bid
            "kraken_best_ask": None,  # Current Kraken best ask
            "ws_funding_rate": None,  # Current funding rate
            "ws_predicted_rate": None,  # Predicted funding rate
            "premium": None,  # Current premium
            "oracle_px": None,  # Current oracle price
            "kraken_pair": kraken_pair,  # Kraken pair for the token
            "price_precision": price_precision,  # Price precision for orders
        }
    
    return tokens

def format_token_dictionary(token_dict):
    """
    Format the token dictionary as a Python code string
    """
    output = "from collections import deque\n\n"
    output += "AVAILABLE_PAIRS = {\n"
    
    for token, data in sorted(token_dict.items()):
        output += f'    "{token}": {{\n'
        
        # Add each field with its comment
        output += f'        "position_size": {data["position_size"]},  # Total position size in USD\n'
        output += f'        "margin_size": {data["margin_size"]},  # Approximate margin required\n'
        output += f'        "hl_order_type": "{data["hl_order_type"]}",  # Use {data["hl_order_type"]} orders on Hyperliquid for {token}\n'
        output += f'        "percentile_threshold": {data["percentile_threshold"]},  # Entry threshold percentile\n'
        output += f'        "websocket_subscribed": {data["websocket_subscribed"]},  # Track subscription status per asset\n'
        output += f'        "in_position": {data["in_position"]},  # Track position status per asset\n'
        output += f'        "hl_position_size": {data["hl_position_size"]},  # Current HL position size\n'
        output += f'        "kraken_position_size": {data["kraken_position_size"]},  # Current Kraken position size\n'
        output += f'        "historical_rates": deque(maxlen=500),  # Historical funding rates\n'
        output += f'        "percentile_60": {data["percentile_60"]},  # 60th percentile threshold\n'
        output += f'        "current_hl_order_id": {data["current_hl_order_id"]},  # Current HL order ID\n'
        output += f'        "current_kraken_order_id": {data["current_kraken_order_id"]},  # Current Kraken order ID\n'
        output += f'        "hl_best_bid": {data["hl_best_bid"]},  # Current HL best bid\n'
        output += f'        "hl_best_ask": {data["hl_best_ask"]},  # Current HL best ask\n'
        output += f'        "kraken_best_bid": {data["kraken_best_bid"]},  # Current Kraken best bid\n'
        output += f'        "kraken_best_ask": {data["kraken_best_ask"]},  # Current Kraken best ask\n'
        output += f'        "ws_funding_rate": {data["ws_funding_rate"]},  # Current funding rate\n'
        output += f'        "ws_predicted_rate": {data["ws_predicted_rate"]},  # Predicted funding rate\n'
        output += f'        "premium": {data["premium"]},  # Current premium\n'
        output += f'        "oracle_px": {data["oracle_px"]},  # Current oracle price\n'
        
        # Handle kraken_pair specially since it might be None
        if data["kraken_pair"] is None:
            output += f'        "kraken_pair": None,  # Kraken pair for {token}\n'
        else:
            output += f'        "kraken_pair": "{data["kraken_pair"]}",  # Kraken pair for {token}\n'
            
        output += f'        "price_precision": {data["price_precision"]},  # Price precision for orders\n'
        output += '    },\n'
    
    output += "}"
    return output

def main():
    """
    Main function to run the script
    """
    # Create the token dictionary using API data
    token_dict = create_token_dictionary()
    
    # Format the output
    formatted_output = format_token_dictionary(token_dict)
    
    # Write to output file
    output_file = "token_dictionary_output.py"
    with open(output_file, 'w') as f:
        f.write(formatted_output)
    
    print(f"Successfully processed {len(token_dict)} tokens.")
    print(f"Output written to '{output_file}'.")

if __name__ == "__main__":
    main()
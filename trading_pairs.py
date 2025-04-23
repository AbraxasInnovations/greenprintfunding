#!/usr/bin/env python3
"""
Trading Pairs Module for Abraxas Greenprint Funding Bot
----------------------------------------------------
Defines available trading pairs and validation functions
"""

import requests
import logging
from typing import List, Dict, Set, Tuple, Optional
from collections import deque

# Configure logging
logger = logging.getLogger(__name__)



AVAILABLE_PAIRS = {
    "AAVE": {
        "description": "Aave",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for AAVE
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "AAVEUSD",  # Kraken pair for AAVE
        "price_precision": 4,  # Price precision for orders
    },
    "ADA": {
        "description": "Cardano",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for ADA
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "ADAUSD",  # Kraken pair for ADA
        "price_precision": 4,  # Price precision for orders
    },
    "ALGO": {
        "description": "Algorand",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for ALGO
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "ALGOUSD",  # Kraken pair for ALGO
        "price_precision": 4,  # Price precision for orders
    },
    "ALT": {
        "description": "Altlayer",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for ALT
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "ALTUSD",  # Kraken pair for ALT
        "price_precision": 4,  # Price precision for orders
    },
    "APE": {
        "description": "ApeCoin",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for APE
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "APEUSD",  # Kraken pair for APE
        "price_precision": 4,  # Price precision for orders
    },
    "APT": {
        "description": "Aptos",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for APT
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "APTUSD",  # Kraken pair for APT
        "price_precision": 4,  # Price precision for orders
    },
    "AR": {
        "description": "AR token",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for AR
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "ARUSD",  # Kraken pair for AR
        "price_precision": 4,  # Price precision for orders
    },
    "ARB": {
        "description": "Arbitrum",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for ARB
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "ARBUSD",  # Kraken pair for ARB
        "price_precision": 4,  # Price precision for orders
    },
    "ATOM": {
        "description": "Cosmos",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for ATOM
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "ATOMUSD",  # Kraken pair for ATOM
        "price_precision": 4,  # Price precision for orders
    },
    "BABY": {
        "description": "BABY token",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for BABY
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "BABYUSD",  # Kraken pair for BABY
        "price_precision": 4,  # Price precision for orders
    },
    "BADGER": {
        "description": "Badger DAO",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for BADGER
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "BADGERUSD",  # Kraken pair for BADGER
        "price_precision": 4,  # Price precision for orders
    },
    "BCH": {
        "description": "Bitcoin Cash",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for BCH
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "BCHUSD",  # Kraken pair for BCH
        "price_precision": 4,  # Price precision for orders
    },
    "BERA": {
        "description": "Bera",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for BERA
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "BERAUSD",  # Kraken pair for BERA
        "price_precision": 4,  # Price precision for orders
    },
    "BIGTIME": {
        "description": "Big Time",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for BIGTIME
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "BIGTIMEUSD",  # Kraken pair for BIGTIME
        "price_precision": 4,  # Price precision for orders
    },
    "BIO": {
        "description": "Biconomy",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for BIO
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "BIOUSD",  # Kraken pair for BIO
        "price_precision": 4,  # Price precision for orders
    },
    "BLUR": {
        "description": "Blur",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for BLUR
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "BLURUSD",  # Kraken pair for BLUR
        "price_precision": 4,  # Price precision for orders
    },
    "BNB": {
        "description": "BNB token",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for BNB
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "BNBUSD",  # Kraken pair for BNB
        "price_precision": 4,  # Price precision for orders
    },
    "BNT": {
        "description": "Bancor",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for BNT
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "BNTUSD",  # Kraken pair for BNT
        "price_precision": 4,  # Price precision for orders
    },
    "CELO": {
        "description": "CELO token",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for CELO
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "CELOUSD",  # Kraken pair for CELO
        "price_precision": 4,  # Price precision for orders
    },
    "COMP": {
        "description": "Compound",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for COMP
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "COMPUSD",  # Kraken pair for COMP
        "price_precision": 4,  # Price precision for orders
    },
    "CRV": {
        "description": "Curve DAO",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for CRV
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "CRVUSD",  # Kraken pair for CRV
        "price_precision": 4,  # Price precision for orders
    },
    "CYBER": {
        "description": "CyberConnect",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for CYBER
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "CYBERUSD",  # Kraken pair for CYBER
        "price_precision": 4,  # Price precision for orders
    },
    "DOT": {
        "description": "Polkadot",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for DOT
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "DOTUSD",  # Kraken pair for DOT
        "price_precision": 4,  # Price precision for orders
    },
    "DYM": {
        "description": "Dymension",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for DYM
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "DYMUSD",  # Kraken pair for DYM
        "price_precision": 4,  # Price precision for orders
    },
    "EIGEN": {
        "description": "EigenLayer",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for EIGEN
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "EIGENUSD",  # Kraken pair for EIGEN
        "price_precision": 4,  # Price precision for orders
    },
    "ENA": {
        "description": "Ethena",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for ENA
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "ENAUSD",  # Kraken pair for ENA
        "price_precision": 4,  # Price precision for orders
    },
    "ENS": {
        "description": "Ethereum Name Service",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for ENS
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "ENSUSD",  # Kraken pair for ENS
        "price_precision": 4,  # Price precision for orders
    },
    "ETC": {
        "description": "Ethereum Classic",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for ETC
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "XETCZUSD",  # Kraken pair for ETC
        "price_precision": 4,  # Price precision for orders
    },
    "ETH": {
        "description": "Ethereum",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for ETH
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "XETHZUSD",  # Kraken pair for ETH
        "price_precision": 2,  # Price precision for orders
    },
    "ETHFI": {
        "description": "ETHfi",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for ETHFI
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "ETHFIUSD",  # Kraken pair for ETHFI
        "price_precision": 4,  # Price precision for orders
    },
    "FARTCOIN": {
        "description": "FARTCOIN token",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for FARTCOIN
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "FARTCOINUSD",  # Kraken pair for FARTCOIN
        "price_precision": 4,  # Price precision for orders
    },
    "FET": {
        "description": "Fetch.ai",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for FET
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "FETUSD",  # Kraken pair for FET
        "price_precision": 4,  # Price precision for orders
    },
    "FIL": {
        "description": "Filecoin",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for FIL
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "FILUSD",  # Kraken pair for FIL
        "price_precision": 4,  # Price precision for orders
    },
    "FTM": {
        "description": "Fantom",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for FTM
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "FTMUSD",  # Kraken pair for FTM
        "price_precision": 4,  # Price precision for orders
    },
    "GALA": {
        "description": "Gala",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for GALA
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "GALAUSD",  # Kraken pair for GALA
        "price_precision": 4,  # Price precision for orders
    },
    "GMT": {
        "description": "STEPN",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for GMT
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "GMTUSD",  # Kraken pair for GMT
        "price_precision": 4,  # Price precision for orders
    },
    "GOAT": {
        "description": "GOAT token",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for GOAT
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "GOATUSD",  # Kraken pair for GOAT
        "price_precision": 4,  # Price precision for orders
    },
    "GRASS": {
        "description": "GRASSHOP",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for GRASS
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "GRASSUSD",  # Kraken pair for GRASS
        "price_precision": 4,  # Price precision for orders
    },
    "GRIFFAIN": {
        "description": "Griffain",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for GRIFFAIN
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "GRIFFAINUSD",  # Kraken pair for GRIFFAIN
        "price_precision": 4,  # Price precision for orders
    },
    "HMSTR": {
        "description": "HMSTR token",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for HMSTR
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "HMSTRUSD",  # Kraken pair for HMSTR
        "price_precision": 4,  # Price precision for orders
    },
    "HPOS": {
        "description": "Harry Potter OSI10",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "market",  # Use market orders on Hyperliquid for HPOS
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "HPOS10IUSD",  # Kraken pair for HPOS
        "price_precision": 2,  # Price precision for orders
    },
    "INJ": {
        "description": "Injective",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for INJ
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "INJUSD",  # Kraken pair for INJ
        "price_precision": 4,  # Price precision for orders
    },
    "IP": {
        "description": "IP token",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for IP
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "IPUSD",  # Kraken pair for IP
        "price_precision": 4,  # Price precision for orders
    },
    "JTO": {
        "description": "Jito",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for JTO
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "JTOUSD",  # Kraken pair for JTO
        "price_precision": 4,  # Price precision for orders
    },
    "JUP": {
        "description": "Jupiter",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for JUP
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "JUPUSD",  # Kraken pair for JUP
        "price_precision": 4,  # Price precision for orders
    },
    "KAITO": {
        "description": "Kaito",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for KAITO
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "KAITOUSD",  # Kraken pair for KAITO
        "price_precision": 4,  # Price precision for orders
    },
    "KAS": {
        "description": "Kaspa",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for KAS
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "KASUSD",  # Kraken pair for KAS
        "price_precision": 4,  # Price precision for orders
    },
    "LAYER": {
        "description": "LAYER token",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for LAYER
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "LAYERUSD",  # Kraken pair for LAYER
        "price_precision": 4,  # Price precision for orders
    },
    "LDO": {
        "description": "Lido DAO",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for LDO
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "LDOUSD",  # Kraken pair for LDO
        "price_precision": 4,  # Price precision for orders
    },
    "LINK": {
        "description": "Chainlink",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for LINK
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "LINKUSD",  # Kraken pair for LINK
        "price_precision": 4,  # Price precision for orders
    },
    "LTC": {
        "description": "Litecoin",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for LTC
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "XLTCZUSD",  # Kraken pair for LTC
        "price_precision": 4,  # Price precision for orders
    },
    "MATIC": {
        "description": "Polygon",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for MATIC
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "MATICUSD",  # Kraken pair for MATIC
        "price_precision": 4,  # Price precision for orders
    },
    "ME": {
        "description": "Magic Eden",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for ME
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "MEUSD",  # Kraken pair for ME
        "price_precision": 4,  # Price precision for orders
    },
    "MELANIA": {
        "description": "MELANIA token",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for MELANIA
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "MELANIAUSD",  # Kraken pair for MELANIA
        "price_precision": 4,  # Price precision for orders
    },
    "MEME": {
        "description": "Meme",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for MEME
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "MEMEUSD",  # Kraken pair for MEME
        "price_precision": 4,  # Price precision for orders
    },
    "MEW": {
        "description": "Mew",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for MEW
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "MEWUSD",  # Kraken pair for MEW
        "price_precision": 4,  # Price precision for orders
    },
    "MINA": {
        "description": "Mina Protocol",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for MINA
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "MINAUSD",  # Kraken pair for MINA
        "price_precision": 4,  # Price precision for orders
    },
    "MKR": {
        "description": "Maker",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for MKR
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "MKRUSD",  # Kraken pair for MKR
        "price_precision": 4,  # Price precision for orders
    },
    "MNT": {
        "description": "Mantle",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for MNT
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "MNTUSD",  # Kraken pair for MNT
        "price_precision": 4,  # Price precision for orders
    },
    "MOODENG": {
        "description": "Moodeng",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for MOODENG
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "MOODENGUSD",  # Kraken pair for MOODENG
        "price_precision": 4,  # Price precision for orders
    },
    "MORPHO": {
        "description": "Morpho",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for MORPHO
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "MORPHOUSD",  # Kraken pair for MORPHO
        "price_precision": 4,  # Price precision for orders
    },
    "MOVE": {
        "description": "Move Network",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for MOVE
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "MOVEUSD",  # Kraken pair for MOVE
        "price_precision": 4,  # Price precision for orders
    },
    "NEAR": {
        "description": "NEAR Protocol",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for NEAR
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "NEARUSD",  # Kraken pair for NEAR
        "price_precision": 4,  # Price precision for orders
    },
    "NIL": {
        "description": "NIL token",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for NIL
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "NILUSD",  # Kraken pair for NIL
        "price_precision": 4,  # Price precision for orders
    },
    "NOT": {
        "description": "Not",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for NOT
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "NOTUSD",  # Kraken pair for NOT
        "price_precision": 4,  # Price precision for orders
    },
    "NTRN": {
        "description": "Neutron",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for NTRN
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "NTRNUSD",  # Kraken pair for NTRN
        "price_precision": 4,  # Price precision for orders
    },
    "OGN": {
        "description": "OGN token",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for OGN
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "OGNUSD",  # Kraken pair for OGN
        "price_precision": 4,  # Price precision for orders
    },
    "OM": {
        "description": "OM",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for OM
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "OMUSD",  # Kraken pair for OM
        "price_precision": 4,  # Price precision for orders
    },
    "OMNI": {
        "description": "OMNI token",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for OMNI
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "OMNIUSD",  # Kraken pair for OMNI
        "price_precision": 4,  # Price precision for orders
    },
    "ONDO": {
        "description": "Ondo Finance",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for ONDO
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "ONDOUSD",  # Kraken pair for ONDO
        "price_precision": 4,  # Price precision for orders
    },
    "OP": {
        "description": "Optimism",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for OP
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "OPUSD",  # Kraken pair for OP
        "price_precision": 4,  # Price precision for orders
    },
    "PENDLE": {
        "description": "Pendle",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for PENDLE
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "PENDLEUSD",  # Kraken pair for PENDLE
        "price_precision": 4,  # Price precision for orders
    },
    "PENGU": {
        "description": "PENGU token",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for PENGU
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "PENGUUSD",  # Kraken pair for PENGU
        "price_precision": 4,  # Price precision for orders
    },
    "PNUT": {
        "description": "PeanutDAO",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for PNUT
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "PNUTUSD",  # Kraken pair for PNUT
        "price_precision": 4,  # Price precision for orders
    },
    "POL": {
        "description": "Polyhedra",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for POL
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "POLUSD",  # Kraken pair for POL
        "price_precision": 4,  # Price precision for orders
    },
    "POPCAT": {
        "description": "POPCAT",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for POPCAT
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "POPCATUSD",  # Kraken pair for POPCAT
        "price_precision": 4,  # Price precision for orders
    },
    "PROMPT": {
        "description": "PROMPT token",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for PROMPT
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "PROMPTUSD",  # Kraken pair for PROMPT
        "price_precision": 4,  # Price precision for orders
    },
    "PYTH": {
        "description": "Pyth Network",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for PYTH
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "PYTHUSD",  # Kraken pair for PYTH
        "price_precision": 4,  # Price precision for orders
    },
    "RENDER": {
        "description": "Render Network",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for RENDER
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "RENDERUSD",  # Kraken pair for RENDER
        "price_precision": 4,  # Price precision for orders
    },
    "REQ": {
        "description": "Request Network",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for REQ
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "REQUSD",  # Kraken pair for REQ
        "price_precision": 4,  # Price precision for orders
    },
    "RSR": {
        "description": "Reserve Rights",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for RSR
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "RSRUSD",  # Kraken pair for RSR
        "price_precision": 4,  # Price precision for orders
    },
    "RUNE": {
        "description": "THORChain",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for RUNE
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "RUNEUSD",  # Kraken pair for RUNE
        "price_precision": 4,  # Price precision for orders
    },
    "SAGA": {
        "description": "Saga",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for SAGA
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "SAGAUSD",  # Kraken pair for SAGA
        "price_precision": 4,  # Price precision for orders
    },
    "SAND": {
        "description": "The Sandbox",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for SAND
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "SANDUSD",  # Kraken pair for SAND
        "price_precision": 4,  # Price precision for orders
    },
    "SEI": {
        "description": "SEI",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for SEI
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "SEIUSD",  # Kraken pair for SEI
        "price_precision": 4,  # Price precision for orders
    },
    "SOL": {
        "description": "Solana",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for SOL
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "SOLUSD",  # Kraken pair for SOL
        "price_precision": 4,  # Price precision for orders
    },
    "STG": {
        "description": "Stargate Finance",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for STG
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "STGUSD",  # Kraken pair for STG
        "price_precision": 4,  # Price precision for orders
    },
    "STRK": {
        "description": "Starknet",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for STRK
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "STRKUSD",  # Kraken pair for STRK
        "price_precision": 4,  # Price precision for orders
    },
    "SUI": {
        "description": "Sui",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for SUI
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "SUIUSD",  # Kraken pair for SUI
        "price_precision": 4,  # Price precision for orders
    },
    "SUPER": {
        "description": "SuperVerse",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for SUPER
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "SUPERUSD",  # Kraken pair for SUPER
        "price_precision": 4,  # Price precision for orders
    },
    "SUSHI": {
        "description": "SushiSwap",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for SUSHI
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "SUSHIUSD",  # Kraken pair for SUSHI
        "price_precision": 4,  # Price precision for orders
    },
    "TAO": {
        "description": "Bittensor",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for TAO
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "TAOUSD",  # Kraken pair for TAO
        "price_precision": 4,  # Price precision for orders
    },
    "TIA": {
        "description": "Celestia",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for TIA
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "TIAUSD",  # Kraken pair for TIA
        "price_precision": 4,  # Price precision for orders
    },
    "TNSR": {
        "description": "Tensor",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for TNSR
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "TNSRUSD",  # Kraken pair for TNSR
        "price_precision": 4,  # Price precision for orders
    },
    "TON": {
        "description": "Toncoin",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for TON
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "TONUSD",  # Kraken pair for TON
        "price_precision": 4,  # Price precision for orders
    },
    "TRUMP": {
        "description": "Trump",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for TRUMP
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "TRUMPUSD",  # Kraken pair for TRUMP
        "price_precision": 4,  # Price precision for orders
    },
    "TURBO": {
        "description": "TurboETH",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for TURBO
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "TURBOUSD",  # Kraken pair for TURBO
        "price_precision": 4,  # Price precision for orders
    },
    "UMA": {
        "description": "UMA token",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for UMA
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "UMAUSD",  # Kraken pair for UMA
        "price_precision": 4,  # Price precision for orders
    },
    "UNI": {
        "description": "Uniswap",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for UNI
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "UNIUSD",  # Kraken pair for UNI
        "price_precision": 4,  # Price precision for orders
    },
    "USUAL": {
        "description": "Usual",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for USUAL
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "USUALUSD",  # Kraken pair for USUAL
        "price_precision": 4,  # Price precision for orders
    },
    "VINE": {
        "description": "VINE token",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for VINE
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "VINEUSD",  # Kraken pair for VINE
        "price_precision": 4,  # Price precision for orders
    },
    "VIRTUAL": {
        "description": "VIRTUAL token",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for VIRTUAL
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "VIRTUALUSD",  # Kraken pair for VIRTUAL
        "price_precision": 4,  # Price precision for orders
    },
    "VVV": {
        "description": "VVV token",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for VVV
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "VVVUSD",  # Kraken pair for VVV
        "price_precision": 4,  # Price precision for orders
    },
    "W": {
        "description": "Wormhole",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for W
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "WUSD",  # Kraken pair for W
        "price_precision": 4,  # Price precision for orders
    },
    "WCT": {
        "description": "WCT token",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for WCT
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "WCTUSD",  # Kraken pair for WCT
        "price_precision": 4,  # Price precision for orders
    },
    "WIF": {
        "description": "Dogwifhat",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for WIF
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "WIFUSD",  # Kraken pair for WIF
        "price_precision": 4,  # Price precision for orders
    },
    "WLD": {
        "description": "WLD token",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for WLD
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "WLDUSD",  # Kraken pair for WLD
        "price_precision": 4,  # Price precision for orders
    },
    "YGG": {
        "description": "YGG token",  # Full name of the token
        "position_size": 12.0,  # Total position size in USD
        "margin_size": 4.0,  # Approximate margin required
        "hl_order_type": "limit",  # Use limit orders on Hyperliquid for YGG
        "percentile_threshold": 60,  # Entry threshold percentile
        "websocket_subscribed": False,  # Track subscription status per asset
        "in_position": False,  # Track position status per asset
        "hl_position_size": 0.0,  # Current HL position size
        "kraken_position_size": 0.0,  # Current Kraken position size
        "historical_rates": deque(maxlen=500),  # Historical funding rates
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
        "kraken_pair": "YGGUSD",  # Kraken pair for YGG
        "price_precision": 4,  # Price precision for orders
    },
}



# Define available trading pairs with their configuration

def get_available_pairs() -> Dict:
    """
    Get all available trading pairs
    
    Returns:
        Dictionary of available pairs with their configurations
    """
    return AVAILABLE_PAIRS

def get_available_pairs_list() -> List[str]:
    """
    Get list of available pairs symbols
    
    Returns:
        List of available pair symbols
    """
    return list(AVAILABLE_PAIRS.keys())

def format_pairs_description() -> str:
    """
    Format available pairs as readable text for Telegram
    
    Returns:
        Formatted string of available pairs with descriptions
    """
    formatted = "📊 *Available Trading Pairs*\n\n"
    
    for symbol, config in AVAILABLE_PAIRS.items():
        special_note = ""
        if symbol == "HYPE":
            special_note = " _(Special: both spot and perp on Hyperliquid)_"
            
        formatted += f"• *{symbol}*: {config['description']}{special_note}\n"
        
    formatted += "\nUse these symbols when selecting tokens for your trading bot."
    return formatted

def validate_pair_selection(pairs: List[str]) -> List[str]:
    """
    Validate a list of user-selected pairs
    
    Args:
        pairs: List of pair symbols selected by user
        
    Returns:
        List of valid pair symbols (invalid ones removed)
    """
    valid_pairs = []
    
    for pair in pairs:
        if pair in AVAILABLE_PAIRS:
            valid_pairs.append(pair)
        else:
            logger.warning(f"Invalid pair selected: {pair}")
            
    return valid_pairs

def check_hyperliquid_perpetuals() -> Set[str]:
    """
    Check which perpetuals are currently available on Hyperliquid
    
    Returns:
        Set of available perpetual symbols on Hyperliquid
    """
    try:
        # Use meta endpoint which is more reliable and doesn't require authentication
        response = requests.post("https://api.hyperliquid.xyz/info", json={"type": "meta"})
        
        if response.status_code == 200:
            data = response.json()
            if 'universe' in data:
                # Extract token names from universe list
                return {coin['name'] for coin in data['universe']}
            else:
                logger.error("No 'universe' field in Hyperliquid API response")
        else:
            logger.error(f"Failed to fetch Hyperliquid perpetuals: {response.status_code}")
            
    except Exception as e:
        logger.error(f"Error checking Hyperliquid perpetuals: {str(e)}")
        
    # Return all tokens in AVAILABLE_PAIRS as default if API call fails
    # This ensures all defined tokens are considered available
    return {k for k in AVAILABLE_PAIRS.keys() if k != "HYPE"}  # All tokens except HYPE (which is special case)

def check_kraken_spot_pairs() -> Set[str]:
    """
    Check which spot pairs are currently available on Kraken
    
    Returns:
        Set of available spot symbols on Kraken
    """
    try:
        response = requests.get("https://api.kraken.com/0/public/AssetPairs")
        
        if response.status_code == 200:
            data = response.json()
            
            if "result" in data:
                # Map Kraken's unusual asset naming to standard symbols
                kraken_to_standard = {
                    # Generate complete mapping from all AVAILABLE_PAIRS
                }
                
                # Automatically populate the mapping from AVAILABLE_PAIRS
                for symbol, config in AVAILABLE_PAIRS.items():
                    if config.get("kraken_pair") is not None:
                        kraken_to_standard[config["kraken_pair"]] = symbol
                
                available_pairs = set()
                for pair_name in data["result"].keys():
                    if pair_name in kraken_to_standard:
                        available_pairs.add(kraken_to_standard[pair_name])
                        
                return available_pairs
            else:
                logger.error("No 'result' field in Kraken API response")
                
        else:
            logger.error(f"Failed to fetch Kraken pairs: {response.status_code}")
            
    except Exception as e:
        logger.error(f"Error checking Kraken pairs: {str(e)}")
        
    # Return default list if API call fails - include all tokens that have kraken_pair defined
    return {symbol for symbol, config in AVAILABLE_PAIRS.items() if config.get("kraken_pair") is not None}

def get_active_trading_pairs() -> List[str]:
    """
    Get tokens available for trading
    
    Returns:
        List of available trading pairs
    """
    try:
        # Return ALL tokens in AVAILABLE_PAIRS
        # This makes all defined tokens available for selection
        return sorted(list(AVAILABLE_PAIRS.keys()))
    except Exception as e:
        logger.error(f"Error getting active trading pairs: {str(e)}")
        # Return all available pairs as fallback
        return sorted(list(AVAILABLE_PAIRS.keys()))
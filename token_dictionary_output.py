from collections import deque

AVAILABLE_PAIRS = {
    "AAVE": {
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
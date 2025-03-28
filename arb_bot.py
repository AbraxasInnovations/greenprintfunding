#!/usr/bin/env python3
"""
Crypto Arbitrage Bot Module
--------------------------
Modified version of the original arbitrage bot with security improvements
"""

import requests
import time
import json
import base64
import hashlib
import hmac
import urllib.parse
import websocket
import threading
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import pytz
from typing import Dict, Optional, Tuple, List, Union, Any
import logging
from logging.handlers import RotatingFileHandler
from collections import deque
import queue
import os
import configparser
from hyperliquid.info import Info
from hyperliquid.utils import constants
from hyperliquid.exchange import Exchange
from eth_account import Account

class ArbBotBase:
    """Base class for arbitrage bots with common functionality"""
    
    def __init__(self, config_path=None, user_id=None):
        # API URLs
        self.hl_ws_url = "wss://api.hyperliquid.xyz/ws"
        self.hl_api_url = "https://api.hyperliquid.xyz/info"
        self.kraken_api_url = "https://api.kraken.com"
        
        # User identification
        self.user_id = user_id or "default"
        self.config_path = config_path
        
        # API credentials (populated by load_credentials)
        self.kraken_key = None
        self.kraken_secret = None
        self.hl_key = None
        self.hl_secret = None
        
        # API clients (initialized in setup_apis)
        self.hl_info = None
        self.hl_exchange = None
        
        # Rate limiting for Kraken API (intermediate tier)
        self.kraken_api_last_call = 0.0
        self.kraken_api_min_interval = 0.35  # ~3 calls per second max (35 / 46 limit with buffer)
        self.kraken_order_check_interval = 3.0  # Check order status every 3 seconds
        self.kraken_call_times = []
        self.kraken_rate_limit_window = 60  # seconds (1-minute window per chart)
        self.kraken_max_calls_per_window = 46  # Total API calls limit for Intermediate tier
        
        # Safety checks and monitoring intervals
        self.last_margin_check_time = 0
        self.margin_check_interval = 60  # seconds between margin checks
        self.min_margin_ratio = 0.15  # 15% margin ratio threshold for liquidation protection
        self.max_price_deviation = 0.05  # 5% max price deviation for flash crash detection
        
        # WebSocket related attributes
        self.ws = None
        self.ws_message_queue = queue.Queue()
        self.ws_reconnect_count = 0
        
        # Trade management
        self.running = True
        self.positions = {}
        self.order_history = {}
        
        # Logger (initialized in setup_logging)
        self.logger = None
        
        # Error handling
        self.consecutive_errors = 0
        self.error_cooldown = 5  # seconds
        self.extended_cooldown = 30  # seconds
        self.max_consecutive_errors = 5
        
        # Performance monitoring
        self.volatility_window = 200  # Number of price data points to store
        self.order_book_cache = {}
        self.historical_percentiles = {}
        self.flash_crash_cooldowns = {}
        
        # Common configuration
        self.exit_time_threshold = 15  # Minutes before hour end to check for exit
        self.order_timeout = 60  # Seconds to wait for order fill
        self.max_retries = 3  # Maximum number of order placement retries
        self.rate_check_interval = 5  # Update last paid rate every 5 seconds
        self.max_ws_reconnects = 10  # Maximum WebSocket reconnection attempts
        self.slippage_buffer = 0.001  # 0.1% slippage buffer for limit orders
        self.min_order_book_depth = 1.5  # Minimum order book depth as multiplier of position size
        
        # Selected tokens list (populated from database or config)
        self.selected_tokens = []
        
        # Custom strategy settings
        self.entry_strategy = "default"  # Default is 60th percentile
        self.exit_strategy = "default"   # Default is before next negative rate
        
        # Entry percentile thresholds
        self.entry_percentiles = {
            "default": 60,
            "50": 50,
            "75": 75,
            "85": 85,
            "95": 95,
            "abraxas": 60  # Same as default
        }
        
        # Exit percentile thresholds
        self.exit_percentiles = {
            "default": None,  # Default uses the next negative rate logic
            "50": 50,
            "35": 35,
            "20": 20,
            "10": 10,
            "abraxas": None  # Same as default
        }
        
        # Initialize trading assets dict (will be populated by child classes)
        self.assets = {}
        self.supported_assets = []
        
        # Data structures for historical data
        self.funding_history = {}
        self.last_funding_rates = {}
        self.last_percentiles = {}
    
    def initialize(self):
        """Initialize the bot after configuration"""
        # Setup logging first to ensure logger is available for all subsequent methods
        self.setup_logging()
        
        self.load_credentials()
        self.load_custom_settings()
        self.setup_apis()
        
        # Filter assets based on selected tokens
        self.filter_assets_by_selected_tokens()
        
        # Calculate historical percentiles for all remaining assets
        for asset in self.assets.keys():
            self.calculate_historical_percentile(asset)
        
        # Start message processing thread
        self.start_message_processor()
    
    def filter_assets_by_selected_tokens(self):
        """Filter assets dictionary to only include selected tokens"""
        self.logger.info(f"Filtering assets based on selected tokens: {self.selected_tokens if hasattr(self, 'selected_tokens') else 'None'}")
        
        # Ensure assets dict is initialized
        if not hasattr(self, 'assets') or not self.assets:
            self.logger.warning("Assets dictionary not initialized, cannot filter assets")
            return {}
            
        if hasattr(self, 'selected_tokens') and self.selected_tokens:
            # Create a new dictionary with only selected tokens
            filtered_assets = {}
            
            # Check which user-selected tokens are available in our supported assets
            available_selected_tokens = []
            for token in self.selected_tokens:
                if token in self.assets:
                    filtered_assets[token] = self.assets[token]
                    available_selected_tokens.append(token)
                    self.logger.info(f"Including selected token: {token}")
                else:
                    self.logger.warning(f"Selected token not supported by this tier: {token}")
            
            self.logger.info(f"User selected tokens: {self.selected_tokens}")
            self.logger.info(f"Available selected tokens: {available_selected_tokens}")
            
            # Special case for Tier 1 - respect the user's selection
            if isinstance(self, Tier1Bot):
                self.logger.info(f"Tier 1 Bot - Available selected tokens: {available_selected_tokens}")
                if available_selected_tokens:
                    # Use the first valid selected token
                    chosen_token = available_selected_tokens[0]
                    self.assets = {chosen_token: filtered_assets[chosen_token]}
                    self.supported_assets = [chosen_token]
                    self.logger.info(f"Tier 1 bot configured for token: {chosen_token}")
                elif "BADGER" in self.assets:
                    # Fallback to BADGER if no valid selected tokens
                    self.assets = {"BADGER": self.assets["BADGER"]}
                    self.supported_assets = ["BADGER"]
                    self.logger.info(f"Tier 1 bot defaulting to BADGER (no valid tokens in selection)")
                elif "HPOS" in self.assets:
                    # Second fallback to HPOS
                    self.assets = {"HPOS": self.assets["HPOS"]}
                    self.supported_assets = ["HPOS"]
                    self.logger.info(f"Tier 1 bot defaulting to HPOS (no valid tokens or BADGER)")
                elif "BTC" in self.assets:
                    # Last resort fallback to BTC
                    self.assets = {"BTC": self.assets["BTC"]}
                    self.supported_assets = ["BTC"]
                    self.logger.info(f"Tier 1 bot defaulting to BTC (last resort - no other tokens available)")
                else:
                    self.logger.error("No valid assets found for Tier 1 bot!")
                
            # For other tiers, keep all available selected tokens
            else:
                if available_selected_tokens:
                    # Filter assets to only include selected ones
                    self.assets = filtered_assets
                    self.supported_assets = available_selected_tokens
                    self.logger.info(f"Bot configured for multiple tokens: {available_selected_tokens}")
                else:
                    self.logger.warning("No valid selected tokens! Keeping all supported assets.")
        else:
            self.logger.warning("No selected tokens provided, using all supported assets")
            
        # Final check of which assets are actually being used
        self.logger.info(f"Final assets used by bot: {list(self.assets.keys())}")
        return self.assets
    
    def load_credentials(self):
        """Load API credentials from configuration"""
        try:
            if self.config_path and os.path.exists(self.config_path):
                config = configparser.ConfigParser()
                config.read(self.config_path)
                
                if 'kraken' in config:
                    self.kraken_key = config['kraken']['api_key']
                    self.kraken_secret = config['kraken']['api_secret']
                    
                if 'hyperliquid' in config:
                    self.hl_key = config['hyperliquid']['api_key']
                    self.hl_secret = config['hyperliquid']['private_key']
                    
                self.logger.info("Loaded credentials from config file")
            else:
                # Fall back to individual files for backward compatibility
                try:
                    from kraken_config import KRAKEN_API_KEY, KRAKEN_API_SECRET
                    self.kraken_key = KRAKEN_API_KEY
                    self.kraken_secret = KRAKEN_API_SECRET
                    
                    from hl_config import HL_API_KEY, HL_API_SECRET
                    self.hl_key = HL_API_KEY
                    self.hl_secret = HL_API_SECRET
                    
                    self.logger.info("Loaded credentials from config modules")
                except ImportError:
                    raise Exception("No valid credentials found. Please provide a config file or modules.")
        except Exception as e:
            self.logger.error(f"Error loading credentials: {e}")
            raise
    
    def load_custom_settings(self):
        """Load custom settings for the user"""
        try:
            # If using a database
            if hasattr(self, 'db') and self.db:
                from database import Database
                db = Database()
                strategies = db.get_user_strategies(int(self.user_id))
                self.entry_strategy = strategies.get('entry_strategy', 'default')
                self.exit_strategy = strategies.get('exit_strategy', 'default')
                
                self.logger.info(
                    f"Loaded custom strategies for user {self.user_id}: "
                    f"entry={self.entry_strategy}, exit={self.exit_strategy}"
                )
            
            # If using config file
            elif self.config_path and os.path.exists(self.config_path):
                config = configparser.ConfigParser()
                config.read(self.config_path)
                
                if 'Strategies' in config:
                    self.entry_strategy = config['Strategies'].get('entry_strategy', 'default')
                    self.exit_strategy = config['Strategies'].get('exit_strategy', 'default')
                    
                    self.logger.info(
                        f"Loaded custom strategies from config: "
                        f"entry={self.entry_strategy}, exit={self.exit_strategy}"
                    )
                    
        except Exception as e:
            self.logger.error(f"Error loading custom settings: {str(e)}")
            # Fall back to defaults
            self.entry_strategy = 'default'
            self.exit_strategy = 'default'
    
    def setup_logging(self):
        """Setup logging configuration with log rotation"""
        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # Setup file handler with rotation (10 MB max size, keep 5 backup logs)
        log_filename = f'arb_bot_{self.user_id}.log'
        file_handler = RotatingFileHandler(
            log_filename,
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        
        # Setup console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # Setup logger
        self.logger = logging.getLogger(f"arb_bot_{self.user_id}")
        self.logger.setLevel(logging.INFO)
        
        # Clear existing handlers to avoid duplicates on reinit
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
            
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def setup_apis(self):
        """Initialize API connections and keys"""
        try:
            # Test Kraken API connection
            test_data = {
                "nonce": str(int(1000*time.time()))
            }
            result = self.kraken_request('/0/private/Balance', test_data)
            if 'error' in result and result['error']:
                raise Exception(f"Kraken API test failed: {result['error']}")
                
            self.logger.info("Successfully connected to Kraken API")
            
            # Initialize Hyperliquid SDK for perpetual futures trading
            from hyperliquid.utils.constants import MAINNET_API_URL
            
            # Clean and validate private key format
            private_key = self.hl_secret.strip().replace('0x', '').lower()
            
            # Ensure key is valid hex
            int(private_key, 16)  # This will raise ValueError if not valid hex
            
            if len(private_key) != 64:
                raise ValueError(f"Private key must be 64 characters (got {len(private_key)})")
                
            wallet = Account.from_key(private_key)
            
            # Initialize Hyperliquid SDK with correct base URL
            self.hl_info = Info(MAINNET_API_URL)
            self.hl_exchange = Exchange(
                base_url=MAINNET_API_URL,
                wallet=wallet
            )
            
            self.logger.info("Successfully initialized Hyperliquid SDK")
            
            # Verify balances are sufficient for trading
            self.check_balances()
            
        except ImportError as e:
            raise Exception(f"Failed to load API configurations: {e}")
        except Exception as e:
            raise Exception(f"Failed to initialize APIs: {e}")
    
    def start_message_processor(self):
        """Start the background thread for processing WebSocket messages"""
        processor_thread = threading.Thread(target=self.process_websocket_messages)
        processor_thread.daemon = True
        processor_thread.start()
        self.logger.info("Started WebSocket message processor thread")
    
    def process_websocket_messages(self):
        """Process WebSocket messages from the queue"""
        while self.running:
            try:
                # Get message from queue with timeout
                try:
                    message = self.ws_message_queue.get(timeout=1)
                except queue.Empty:
                    continue
                
                # Process the message
                data = json.loads(message)
                if data.get('channel') == 'activeAssetCtx':
                    ctx = data.get('data', {}).get('ctx', {})
                    coin = data.get('data', {}).get('coin')
                    
                    if coin and coin in self.assets and ctx:
                        asset_data = self.assets[coin]
                        
                        if 'funding' in ctx:
                            asset_data["ws_funding_rate"] = float(ctx['funding'])
                            
                        if 'predFunding' in ctx:
                            asset_data["ws_predicted_rate"] = float(ctx['predFunding'])
                            
                        if 'impactPxs' in ctx:
                            # Store previous prices for flash crash detection
                            if 'hl_best_bid' in asset_data and asset_data["hl_best_bid"]:
                                asset_data["previous_bid"] = asset_data["hl_best_bid"]
                            if 'hl_best_ask' in asset_data and asset_data["hl_best_ask"]:
                                asset_data["previous_ask"] = asset_data["hl_best_ask"]
                                
                            # Update current prices
                            asset_data["hl_best_bid"] = float(ctx['impactPxs'][0])
                            asset_data["hl_best_ask"] = float(ctx['impactPxs'][1])
                            
                            # NEW: Check for flash crash
                            self.check_for_flash_crash(coin)
                            
                        if 'premium' in ctx:
                            asset_data["premium"] = float(ctx['premium'])
                            
                        if 'oraclePx' in ctx:
                            asset_data["oracle_px"] = float(ctx['oraclePx'])
                        
                        # Store price in historical prices array for volatility calculation
                        if 'historical_prices' not in asset_data:
                            asset_data['historical_prices'] = deque(maxlen=self.volatility_window)
                            
                        if asset_data["hl_best_bid"] and asset_data["hl_best_ask"]:
                            mid_price = (asset_data["hl_best_bid"] + asset_data["hl_best_ask"]) / 2
                            asset_data['historical_prices'].append(mid_price)
                
                # Mark task as done
                self.ws_message_queue.task_done()
                
                # Reset consecutive error counter on successful message processing
                self.consecutive_errors = 0
                
            except Exception as e:
                self.logger.error(f"Error processing WebSocket message: {e}")
                self.consecutive_errors += 1
                
                # Apply cooldown if too many consecutive errors
                if self.consecutive_errors >= self.max_consecutive_errors:
                    self.logger.warning(f"Too many consecutive errors ({self.consecutive_errors}), applying extended cooldown")
                    time.sleep(self.extended_cooldown)
                    self.consecutive_errors = 0
                else:
                    time.sleep(self.error_cooldown)
    
    def check_for_flash_crash(self, asset: str):
        """
        Check for sudden large price movements that could indicate a flash crash
        
        Args:
            asset: Asset symbol to check
        """
        asset_data = self.assets[asset]
        
        # Skip if we don't have previous prices
        if not all([
            'previous_bid' in asset_data,
            'previous_ask' in asset_data,
            asset_data["previous_bid"],
            asset_data["previous_ask"],
            asset_data["hl_best_bid"],
            asset_data["hl_best_ask"]
        ]):
            return
        
        # Calculate percentage changes
        bid_change = abs(asset_data["hl_best_bid"] / asset_data["previous_bid"] - 1)
        ask_change = abs(asset_data["hl_best_ask"] / asset_data["previous_ask"] - 1)
        
        # If either bid or ask changed by more than the threshold, trigger flash crash protection
        if bid_change > self.max_price_deviation or ask_change > self.max_price_deviation:
            self.logger.warning(
                f"⚠️ FLASH CRASH PROTECTION TRIGGERED for {asset}: "
                f"Bid change: {bid_change:.2%}, Ask change: {ask_change:.2%}"
            )
            
            # Set flash crash flag
            asset_data["flash_crash_detected"] = True
            asset_data["flash_crash_time"] = time.time()
            
            # If in position, consider emergency exit
            if asset_data["in_position"]:
                self.logger.warning(f"⚠️ Flash crash during active position for {asset}, monitoring closely")
    
    def check_margin_levels(self):
        """Check margin levels to prevent liquidation"""
        current_time = time.time()
        
        # Only check at specified intervals
        if current_time - self.last_margin_check_time < self.margin_check_interval:
            return
            
        self.last_margin_check_time = current_time
        
        try:
            # Get account status from Hyperliquid
            account_info = self.hl_exchange.status()
            
            if not account_info:
                self.logger.error("Failed to get account status")
                return
                
            # Check if margin ratio is available
            if 'marginRatio' in account_info:
                margin_ratio = float(account_info['marginRatio'])
                self.logger.info(f"Current margin ratio: {margin_ratio:.2%}")
                
                # If margin ratio is below threshold, take protective action
                if margin_ratio < self.min_margin_ratio:
                    self.logger.critical(
                        f"⚠️ LIQUIDATION PROTECTION TRIGGERED: "
                        f"Margin ratio {margin_ratio:.2%} below threshold {self.min_margin_ratio:.2%}"
                    )
                    
                    # Close all positions to prevent liquidation
                    self.emergency_close_all_positions()
                    
        except Exception as e:
            self.logger.error(f"Error checking margin levels: {e}")
    
    def emergency_close_all_positions(self):
        """Emergency close all positions to prevent liquidation"""
        self.logger.warning("EMERGENCY CLOSING ALL POSITIONS")
        
        for asset in self.assets:
            asset_data = self.assets[asset]
            if asset_data["in_position"]:
                self.logger.warning(f"Emergency closing {asset} position")
                try:
                    # First close Hyperliquid position
                    hl_success = self.close_hl_position(asset)
                    
                    # Then close Kraken position
                    if asset_data["kraken_position_size"] > 0:
                        kraken_success, _ = self.place_kraken_order(
                            asset=asset,
                            is_entry=False,
                            position_size=asset_data["kraken_position_size"]
                        )
                        
                        if not kraken_success:
                            self.logger.error(f"Failed to close Kraken position for {asset}")
                    
                    # Mark position as closed regardless of success
                    # (we'll resynchronize later)
                    asset_data["in_position"] = False
                    asset_data["hl_position_size"] = 0.0
                    asset_data["kraken_position_size"] = 0.0
                    
                except Exception as e:
                    self.logger.error(f"Error in emergency close for {asset}: {e}")
                    
        self.logger.warning("Emergency position closing completed")
    
    def enforce_kraken_rate_limit(self):
        """Enforce Kraken API rate limits by adding delays between calls"""
        current_time = time.time()
        time_since_last_call = current_time - self.kraken_api_last_call
        
        # If we've made a call recently, sleep to respect the rate limit
        if time_since_last_call < self.kraken_api_min_interval:
            sleep_time = self.kraken_api_min_interval - time_since_last_call
            time.sleep(sleep_time)
            
        # Update last call time
        self.kraken_api_last_call = time.time()
    
    def check_balances(self):
        """Verify sufficient USD balance before trading"""
        try:
            # Check Kraken USD balance
            kraken_balance = self.kraken_request('/0/private/Balance', {"nonce": str(int(1000*time.time()))})
            
            if 'error' in kraken_balance and kraken_balance['error']:
                self.logger.error(f"Failed to get Kraken balance: {kraken_balance['error']}")
                return False
                
            if 'result' in kraken_balance:
                # Get USD balance (Kraken uses ZUSD for USD)
                usd_balance = float(kraken_balance['result'].get('ZUSD', 0))
                self.logger.info(f"Kraken USD balance: ${usd_balance:.2f}")
                
                # If assets are not yet initialized or empty, we can't check position sizes
                if not hasattr(self, 'assets') or not self.assets:
                    self.logger.info("Assets not yet initialized, skipping position size check")
                    return True
                
                # Check if balance is sufficient for all assets combined
                try:
                    total_required = sum(asset_data.get("position_size", 0) for asset_data in self.assets.values())
                    
                    if usd_balance < total_required:
                        self.logger.warning(f"Insufficient USD balance (${usd_balance:.2f}) for total position size (${total_required:.2f})")
                        return False
                except (AttributeError, TypeError) as e:
                    self.logger.warning(f"Could not calculate required balance: {e}")
                    # Continue without balance check if there's an issue with assets structure
                    return True
                    
                return True
                
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking balances: {e}")
            return False
    
    def get_recent_volatility(self, asset: str) -> float:
        """
        Calculate recent volatility for an asset
        
        Args:
            asset: Asset symbol
            
        Returns:
            Recent volatility as a percentage
        """
        asset_data = self.assets[asset]
        
        if 'historical_prices' not in asset_data or len(asset_data['historical_prices']) < 2:
            return self.slippage_buffer  # Default to base slippage if not enough data
            
        prices = list(asset_data['historical_prices'])
        returns = [prices[i]/prices[i-1] - 1 for i in range(1, len(prices))]
        volatility = np.std(returns) * 100  # Convert to percentage
        
        # Cap at reasonable values
        return min(max(volatility, self.slippage_buffer), 0.01)  # Between base slippage and 1%
    
    def execute_with_cooldown(self, func, *args, **kwargs):
        """
        Execute a function with cooldown on errors
        
        Args:
            func: Function to execute
            *args: Arguments to pass to function
            **kwargs: Keyword arguments to pass to function
            
        Returns:
            Result of function or None on error
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.logger.error(f"Function execution failed: {e}, backing off for {self.error_cooldown} seconds")
            self.consecutive_errors += 1
            
            # Apply extended cooldown if too many consecutive errors
            if self.consecutive_errors >= self.max_consecutive_errors:
                self.logger.warning(f"Too many consecutive errors ({self.consecutive_errors}), applying extended cooldown")
                time.sleep(self.extended_cooldown)
                self.consecutive_errors = 0
            else:
                time.sleep(self.error_cooldown)
                
            return None
    
    def calculate_historical_percentile(self, asset: str):
        """
        Calculate historical percentiles for funding rates
        
        Args:
            asset: The asset to calculate percentiles for
        """
        try:
            # If we don't have enough historical data, skip
            if len(self.funding_history[asset]) < 24:  # At least 24 hours of data
                self.logger.info(f"Not enough historical data for {asset} to calculate percentiles")
                return
                
            # Calculate percentiles for all thresholds we use
            rates = [rate for timestamp, rate in self.funding_history[asset]]
            
            if not rates:
                return
                
            # Calculate all percentiles needed for our strategies
            percentiles = {}
            for p in [10, 20, 35, 50, 60, 75, 85, 95]:
                percentiles[p] = np.percentile(rates, p)
                
            # Store the calculated percentiles
            self.last_percentiles[asset] = {}
            for p, value in percentiles.items():
                self.last_percentiles[asset][p] = value
                
            # Calculate current percentile
            current_rate = self.last_funding_rates.get(asset, 0)
            if current_rate > 0:
                # Count how many historical rates are below the current rate
                below_current = sum(1 for r in rates if r < current_rate)
                current_percentile = (below_current / len(rates)) * 100
                self.last_percentiles[asset]['current'] = current_percentile
                
                self.logger.info(
                    f"{asset} Current rate {current_rate:.4f}% is at the {current_percentile:.1f}th percentile"
                )
                
                # Log the thresholds we care about for strategies
                self.logger.debug(
                    f"{asset} Percentiles: " 
                    f"P50={percentiles[50]:.4f}%, "
                    f"P60={percentiles[60]:.4f}%, "
                    f"P75={percentiles[75]:.4f}%, " 
                    f"P85={percentiles[85]:.4f}%, "
                    f"P95={percentiles[95]:.4f}%"
                )
            
        except Exception as e:
            self.logger.error(f"Error calculating percentiles for {asset}: {str(e)}")
            # Ensure we have some default values
            if asset not in self.last_percentiles:
                self.last_percentiles[asset] = {}
    
    def connect_websocket(self):
        """Connect to WebSocket with auto-reconnect and retry limits"""
        # Close existing WebSocket connection if it exists
        if self.ws:
            self.logger.warning("Closing existing WebSocket before reconnecting")
            try:
                self.ws.close()
                time.sleep(1)  # Wait for closure to complete
            except Exception as e:
                self.logger.error(f"Error closing existing WebSocket: {e}")
                
        if self.ws_reconnect_count >= self.max_ws_reconnects:
            self.logger.error(f"Exceeded maximum WebSocket reconnection attempts ({self.max_ws_reconnects})")
            return False
            
        # Reset subscription status for all assets
        for asset in self.assets:
            self.assets[asset]["websocket_subscribed"] = False
            
        self.ws = websocket.WebSocketApp(
            self.hl_ws_url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )
        
        wst = threading.Thread(target=self.ws.run_forever)
        wst.daemon = True
        wst.start()
        
        self.ws_reconnect_count += 1
        return True
    
    def on_message(self, ws, message):
        """Handle WebSocket messages by adding to queue"""
        try:
            # Add message to queue instead of processing directly
            self.ws_message_queue.put(message)
        except Exception as e:
            self.logger.error(f"Error adding WebSocket message to queue: {e}")
    
    def on_error(self, ws, error):
        self.logger.error(f"WebSocket error: {error}")
    
    def on_close(self, ws, close_status_code, close_msg):
        self.logger.warning(f"WebSocket closed: {close_status_code} - {close_msg}")
        
        # Reset subscription status for all assets
        for asset in self.assets:
            self.assets[asset]["websocket_subscribed"] = False
            
        if self.running:
            self.logger.info("Attempting to reconnect...")
            time.sleep(2)  # Wait before reconnecting
            self.connect_websocket()
    
    def on_open(self, ws):
        self.logger.info("WebSocket connected")
        
        # Wait a moment before subscribing to prevent subscription issues
        time.sleep(1)
        
        # Subscribe to all assets
        for asset in self.assets:
            if not self.assets[asset]["websocket_subscribed"]:
                subscribe_msg = {
                    "method": "subscribe",
                    "subscription": {
                        "type": "activeAssetCtx",
                        "coin": asset
                    }
                }
                ws.send(json.dumps(subscribe_msg))
                self.assets[asset]["websocket_subscribed"] = True
                self.logger.info(f"Subscribed to {asset} updates")
                
        # Reset reconnect count on successful connection
        self.ws_reconnect_count = 0
    
    def check_conditions(self):
        """Check entry and exit conditions for all assets"""
        try:
            # Check rate update interval
            current_time = time.time()
            
            if current_time - self.last_rate_check_time >= self.rate_check_interval:
                self.last_rate_check_time = current_time
                
                # Check margin levels periodically
                self.check_margin_levels()
                
                # Check each asset for entry/exit conditions
                for asset in self.assets:
                    asset_data = self.assets[asset]
                    
                    # Skip if flash crash cooldown is active
                    if self.is_flash_crash_cooldown_active(asset):
                        continue
                        
                    if not asset_data["in_position"]:
                        self.check_entry_conditions(asset)
                    else:
                        self.check_exit_conditions(asset)
                        
        except Exception as e:
            self.logger.error(f"Error checking conditions: {e}")
    
    def is_flash_crash_cooldown_active(self, asset: str) -> bool:
        """
        Check if flash crash cooldown is active for an asset
        
        Args:
            asset: Asset symbol
            
        Returns:
            True if cooldown is active, False otherwise
        """
        asset_data = self.assets[asset]
        
        if asset_data.get("flash_crash_detected", False):
            cooldown_elapsed = time.time() - asset_data.get("flash_crash_time", 0)
            
            if cooldown_elapsed < self.flash_crash_cooldown:
                remaining = self.flash_crash_cooldown - cooldown_elapsed
                self.logger.debug(f"{asset} Flash crash cooldown active, {int(remaining)}s remaining")
                return True
            else:
                # Reset flash crash flag after cooldown
                asset_data["flash_crash_detected"] = False
                self.logger.info(f"{asset} Flash crash cooldown expired, resuming normal operation")
                
        return False
    
    def check_entry_conditions(self, asset: str):
        """
        Check if entry conditions are met for an asset
        
        Args:
            asset: The asset to check
            
        Returns:
            True if conditions are met, False otherwise
        """
        # Skip if asset not in selected tokens
        if asset not in self.selected_tokens:
            return False
        
        # Skip if already in a position
        if asset in self.active_positions:
            return False
        
        # Skip if a flash crash cooldown is active
        if self.is_flash_crash_cooldown_active(asset):
            return False
        
        # Check if time is right (avoid entering close to funding time)
        current_time = datetime.now(pytz.utc)
        minutes_to_hour = (60 - current_time.minute) % 60
        if minutes_to_hour < self.exit_time_threshold:
            return False
        
        # Get current funding rate percentile
        percentile = self.last_percentiles.get(asset, 0)
        current_rate = self.last_funding_rates.get(asset, 0)
        
        # Apply the selected entry strategy
        entry_threshold = self.entry_percentiles.get(self.entry_strategy, 60)
        
        # Check if we meet the entry percentile threshold
        if percentile < entry_threshold:
            return False
        
        # Make sure the rate is positive
        if current_rate <= 0:
            return False
        
        # If volatility is too high, skip
        volatility = self.get_recent_volatility(asset)
        if volatility > self.max_volatility:
            self.logger.info(f"Skipping {asset}: volatility {volatility:.4f} > {self.max_volatility:.4f}")
            return False
        
        self.logger.info(
            f"Entry conditions met for {asset}: percentile {percentile:.1f} >= {entry_threshold}, "
            f"rate {current_rate:.4f}%, volatility {volatility:.4f}"
        )
        return True
    
    def check_exit_conditions(self, asset: str):
        """
        Check if exit conditions are met for an asset
        
        Args:
            asset: The asset to check
            
        Returns:
            True if conditions are met, False otherwise
        """
        # Skip if not in position
        if asset not in self.active_positions:
            return False
        
        # Default exit strategy: Exit before next negative funding rate
        if self.exit_strategy == 'default' or self.exit_strategy == 'abraxas':
            # Exit if close to the hour and funding rate is negative or low
            current_time = datetime.now(pytz.utc)
            minutes_to_hour = (60 - current_time.minute) % 60
            current_rate = self.last_funding_rates.get(asset, 0)
            
            if minutes_to_hour <= self.exit_time_threshold and current_rate < 0.01:
                self.logger.info(
                    f"Exit condition met for {asset}: {minutes_to_hour} min to hour, "
                    f"rate {current_rate:.4f}%"
                )
                return True
                
            # Also exit if rate turns significantly negative any time
            if current_rate < -0.02:
                self.logger.info(f"Exit condition met for {asset}: rate turned negative {current_rate:.4f}%")
                return True
                
            return False
            
        # Custom percentile-based exit strategy
        else:
            # Get current percentile
            percentile = self.last_percentiles.get(asset, 100)
            
            # Get exit threshold
            exit_threshold = self.exit_percentiles.get(self.exit_strategy, 50)
            
            # Exit if percentile falls below threshold
            if percentile <= exit_threshold:
                self.logger.info(
                    f"Exit condition met for {asset}: percentile {percentile:.1f} <= {exit_threshold}"
                )
                return True
                
            return False
    
    def calculate_position_size(self, asset: str, price: float) -> float:
        """
        Calculate position size with appropriate precision
        
        Args:
            asset: Asset symbol
            price: Current price of the asset
            
        Returns:
            Position size with appropriate precision
        """
        # Get position size from asset configuration
        position_size = self.assets[asset]["position_size"]
        
        # Calculate raw size
        raw_size = position_size / price
        
        # Round to appropriate precision based on asset
        if asset == "BTC":
            # Bitcoin typically uses 8 decimal places
            return round(raw_size, 8)
        else:
            # Most other cryptocurrencies use 6 decimal places
            return round(raw_size, 6)
    
    def enter_positions(self, asset: str):
        """
        Enter arbitrage positions for the specified asset:
        - Buy spot on Kraken
        - Sell perpetual futures on Hyperliquid
        """
        try:
            asset_data = self.assets[asset]
            
            if asset_data["in_position"]:
                self.logger.warning(f"{asset} Already in position, cannot enter again")
                return
                
            # First place Kraken spot buy order
            kraken_success, kraken_size = self.place_kraken_order(
                asset=asset,
                is_entry=True
            )
            
            if kraken_success and kraken_size > 0:
                self.logger.info(f"{asset} Kraken order filled with size {kraken_size}")
                
                # Then place Hyperliquid perpetual sell order with EXACT same size as the actual filled Kraken order
                hl_success, hl_size = self.place_hl_order(
                    asset=asset,
                    is_entry=True,
                    position_size=kraken_size  # Use actual filled size, not theoretical size
                )
                
                if hl_success and abs(hl_size - kraken_size) < 0.001:  # Ensure sizes match
                    asset_data["in_position"] = True
                    asset_data["hl_position_size"] = hl_size
                    asset_data["kraken_position_size"] = kraken_size
                    asset_data["entry_time"] = datetime.now()
                    self.logger.info(f"{asset} Successfully entered arbitrage position: HL={hl_size}, Kraken={kraken_size}")
                else:
                    # If Hyperliquid order fails or size mismatch, close Kraken position
                    self.logger.error(f"{asset} Hyperliquid entry failed or size mismatch (HL: {hl_size}, Kraken: {kraken_size}), closing Kraken position")
                    self.place_kraken_order(
                        asset=asset,
                        is_entry=False,
                        position_size=kraken_size
                    )
            else:
                self.logger.error(f"{asset} Failed to enter Kraken spot position")
                
        except Exception as e:
            self.logger.error(f"Error entering {asset} positions: {e}")
            # Apply cooldown on error
            time.sleep(self.error_cooldown)
    
    def exit_positions(self, asset: str):
        """
        Exit arbitrage positions for the specified asset:
        - Close Hyperliquid short first (buying back)
        - Then close Kraken spot position (selling)
        """
        try:
            asset_data = self.assets[asset]
            
            if not asset_data["in_position"]:
                self.logger.warning(f"{asset} Not in position, nothing to exit")
                return
                
            # First close Hyperliquid perpetual position
            hl_success, hl_closed_size = self.place_hl_order(
                asset=asset,
                is_entry=False,
                position_size=asset_data["hl_position_size"]
            )
            
            if hl_success:
                # Then close Kraken spot position
                kraken_success, kraken_closed_size = self.place_kraken_order(
                    asset=asset,
                    is_entry=False,
                    position_size=asset_data["kraken_position_size"]
                )
                
                if kraken_success:
                    asset_data["in_position"] = False
                    self.logger.info(f"{asset} Successfully exited positions: HL={hl_closed_size}, Kraken={kraken_closed_size}")
                    asset_data["hl_position_size"] = 0.0
                    asset_data["kraken_position_size"] = 0.0
                else:
                    # If Kraken exit fails, re-enter Hyperliquid to balance
                    self.logger.error(f"{asset} Failed to exit Kraken, attempting to re-short on Hyperliquid")
                    re_entry_success, _ = self.place_hl_order(
                        asset=asset,
                        is_entry=True,
                        position_size=hl_closed_size
                    )
                    
                    if re_entry_success:
                        self.logger.info(f"{asset} Successfully re-entered Hyperliquid position to maintain balance")
                    else:
                        self.logger.critical(f"{asset} RISK EXPOSURE: Failed to re-enter Hyperliquid position after Kraken exit failure")
            else:
                self.logger.error(f"{asset} Failed to exit Hyperliquid position, keeping both positions open")
                
        except Exception as e:
            self.logger.error(f"Error exiting {asset} positions: {e}")
            # Apply cooldown on error
            time.sleep(self.error_cooldown)
    
    def get_kraken_signature(self, urlpath: str, data: dict) -> str:
        """Generate Kraken API signature with proper encoding"""
        post_data = urllib.parse.urlencode(data, doseq=True)
        encoded = (str(data['nonce']).encode() + post_data.encode())
        message = urlpath.encode() + hashlib.sha256(encoded).digest()
        mac = hmac.new(base64.b64decode(self.kraken_secret), message, hashlib.sha512)
        return base64.b64encode(mac.digest()).decode()
    
    def kraken_request(self, uri_path: str, data: dict) -> dict:
        """Make authenticated request to Kraken API with rate limit enforcement"""
        self.enforce_kraken_rate_limit()  # Enforce rate limit before making request
        
        max_retries = 3
        base_delay = 1.0
        
        for attempt in range(max_retries):
            try:
                headers = {
                    'API-Key': self.kraken_key,
                    'API-Sign': self.get_kraken_signature(uri_path, data)
                }
                
                response = requests.post(
                    self.kraken_api_url + uri_path,
                    headers=headers,
                    data=data
                )
                
                if response.ok:
                    result = response.json()
                    
                    # Check for rate limit errors
                    if 'error' in result and any('Rate limit' in error for error in result.get('error', [])):
                        delay = base_delay * (2 ** attempt) + random.uniform(0.5, 2.0)
                        self.logger.warning(f"Rate limit hit, waiting {delay:.2f} seconds...")
                        time.sleep(delay)
                        continue
                        
                    return result
                else:
                    self.logger.error(f"Kraken API error: {response.status_code} - {response.text}")
                    
                    # Retry with exponential backoff
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt) + random.uniform(0.5, 1.0)
                        self.logger.info(f"Retrying in {delay:.2f} seconds...")
                        time.sleep(delay)
                        
            except Exception as e:
                self.logger.error(f"Kraken request error: {e}")
                
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt) + random.uniform(0.5, 1.0)
                    self.logger.info(f"Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                    
        return {"error": ["Max retries exceeded"]}
    
    def get_kraken_ticker(self, asset: str) -> Tuple[Optional[float], Optional[float]]:
        """
        Get current bid/ask for trading pair on Kraken
        
        Args:
            asset: Asset symbol
            
        Returns:
            Tuple of (bid price, ask price)
        """
        try:
            # Get correct Kraken trading pair from asset data
            kraken_pair = self.assets[asset]["kraken_pair"]
            
            response = requests.get(
                f"{self.kraken_api_url}/0/public/Ticker?pair={kraken_pair}"
            )
            
            if not response.ok:
                self.logger.error(f"Kraken ticker API error for {asset}: {response.status_code} - {response.text}")
                return None, None
                
            data = response.json()
            
            if 'result' in data and kraken_pair in data['result']:
                ticker = data['result'][kraken_pair]
                return float(ticker['b'][0]), float(ticker['a'][0])  # bid, ask
                
            return None, None
            
        except Exception as e:
            self.logger.error(f"Error getting Kraken ticker for {asset}: {e}")
            return None, None
    
    def update_kraken_prices(self, asset: str):
        """Update Kraken's best bid/ask prices for the specified asset"""
        bid, ask = self.get_kraken_ticker(asset)
        self.assets[asset]["kraken_best_bid"] = bid
        self.assets[asset]["kraken_best_ask"] = ask
        
        # Store previous prices for flash crash detection (if not already stored)
        if bid and 'kraken_previous_bid' not in self.assets[asset]:
            self.assets[asset]['kraken_previous_bid'] = bid
        if ask and 'kraken_previous_ask' not in self.assets[asset]:
            self.assets[asset]['kraken_previous_ask'] = ask
            
        # Check for flash crash on Kraken side
        if bid and ask and 'kraken_previous_bid' in self.assets[asset] and 'kraken_previous_ask' in self.assets[asset]:
            bid_change = abs(bid / self.assets[asset]['kraken_previous_bid'] - 1)
            ask_change = abs(ask / self.assets[asset]['kraken_previous_ask'] - 1)
            
            if bid_change > self.max_price_deviation or ask_change > self.max_price_deviation:
                self.logger.warning(
                    f"⚠️ FLASH CRASH PROTECTION TRIGGERED on Kraken for {asset}: "
                    f"Bid change: {bid_change:.2%}, Ask change: {ask_change:.2%}"
                )
                
                # Set flash crash flag
                self.assets[asset]["flash_crash_detected"] = True
                self.assets[asset]["flash_crash_time"] = time.time()
                
            # Update previous prices
            self.assets[asset]['kraken_previous_bid'] = bid
            self.assets[asset]['kraken_previous_ask'] = ask
    
    def get_hl_order_book(self, asset: str, depth: int = 10) -> Optional[Dict[str, List]]:
        """
        Get Hyperliquid order book with specified depth
        
        Args:
            asset: Asset symbol
            depth: Number of price levels to fetch
            
        Returns:
            Order book data or None if error
        """
        try:
            payload = {
                "type": "l2Book",
                "coin": asset
            }
            
            response = requests.post(self.hl_api_url, json=payload)
            
            if not response.ok:
                self.logger.error(f"Order book API error for {asset}: {response.status_code} - {response.text}")
                return None
                
            book_data = response.json()
            
            # Transform into a simplified format
            asks = [(float(level['px']), float(level['sz'])) for level in book_data.get('asks', [])[:depth]]
            bids = [(float(level['px']), float(level['sz'])) for level in book_data.get('bids', [])[:depth]]
            
            return {
                'asks': asks,
                'bids': bids
            }
            
        except Exception as e:
            self.logger.error(f"Error getting order book for {asset}: {e}")
            return None
    
    def check_book_depth(self, asset: str, is_buy: bool, size: float) -> Tuple[bool, float]:
        """
        Check if there's enough liquidity in the order book
        
        Args:
            asset: Asset symbol
            is_buy: True if buying, False if selling
            size: Position size to check
            
        Returns:
            Tuple of (has_liquidity, adjusted_price)
        """
        try:
            book = self.get_hl_order_book(asset, depth=20)
            
            if not book:
                return False, 0.0
                
            levels = book['asks'] if is_buy else book['bids']
            required_size = size * self.min_order_book_depth  # Apply multiplier for safety
            
            # Calculate cumulative size and average price
            cumulative_size = 0
            weighted_price = 0
            
            for price, level_size in levels:
                available = min(level_size, required_size - cumulative_size)
                weighted_price += price * available
                cumulative_size += available
                
                if cumulative_size >= required_size:
                    break
                    
            if cumulative_size < required_size:
                self.logger.warning(f"{asset} Insufficient liquidity: required {required_size}, available {cumulative_size}")
                return False, 0.0
                
            avg_price = weighted_price / cumulative_size
            
            self.logger.info(f"{asset} Order book depth check passed: {cumulative_size} available at avg price {avg_price:.4f}")
            return True, avg_price
            
        except Exception as e:
            self.logger.error(f"Error checking order book depth for {asset}: {e}")
            return False, 0.0
    
    def place_hl_order(self, asset: str, is_entry: bool, position_size: float) -> Tuple[bool, float]:
        """
        Place order on Hyperliquid using the appropriate strategy for the asset
        
        Args:
            asset: Asset symbol
            is_entry: True for entry (sell), False for exit (buy)
            position_size: Exact size to trade
            
        Returns:
            Tuple of (success status, order size)
        """
        try:
            asset_data = self.assets[asset]
            
            side = "Sell" if is_entry else "Buy"
            order_type = asset_data["hl_order_type"]
            
            # Ensure we have current prices
            if not all([asset_data["hl_best_bid"], asset_data["hl_best_ask"]]):
                self.logger.error(f"{asset} No valid prices available for order")
                return False, 0.0
                
            # Ensure position size is valid
            if position_size <= 0:
                self.logger.error(f"{asset} Invalid order size: {position_size}")
                return False, 0.0
                
            # Set maximum retries based on order type
            max_retries = self.max_retries if order_type == "limit" else 1
            
            for attempt in range(max_retries):
                try:
                    # Set leverage to 3x for entry
                    if is_entry:
                        self.logger.info(f"{asset} Setting leverage to 3x...")
                        leverage_response = self.hl_exchange.update_leverage(3, asset)
                        
                        # Check for success
                        if not leverage_response or 'error' in leverage_response:
                            self.logger.error(f"{asset} Failed to set leverage: {leverage_response}")
                            if attempt < max_retries - 1:
                                time.sleep(1)
                                continue
                            return False, 0.0
                            
                    # FIX #2: Dynamic slippage based on volatility
                    slippage_factor = self.get_recent_volatility(asset)
                    self.logger.info(f"{asset} Using dynamic slippage factor: {slippage_factor:.4f}%")
                    
                    # Place order using appropriate strategy for the asset
                    if order_type == "market":
                        # For HPOS - Use market orders
                        self.logger.info(f"{asset} Placing Hyperliquid {side} MARKET order: Size={position_size}")
                        order_response = self.hl_exchange.order(
                            asset,
                            not is_entry,  # is_buy (False for entry/sell, True for exit/buy)
                            position_size,
                            None,  # No price for market orders
                            {"market": {}}  # Market order type
                        )
                        
                        # Check response for success
                        if order_response and 'status' in order_response and order_response['status'] == 'success':
                            self.logger.info(f"{asset} Hyperliquid {side} market order executed successfully")
                            
                            # Market orders execute immediately, verify position was created
                            time.sleep(1)  # Short wait for position to be reflected
                            actual_size = self.verify_hl_position(asset, is_entry)
                            
                            if actual_size is not None:
                                return True, actual_size
                            else:
                                return False, 0.0
                        else:
                            self.logger.error(f"{asset} Error placing HL market order: {order_response}")
                            return False, 0.0
                    else:
                        # For BTC - Use limit orders with order book depth check
                        
                        # Check order book depth
                        has_liquidity, avg_price = self.check_book_depth(asset, not is_entry, position_size)
                        
                        if not has_liquidity:
                            self.logger.error(f"{asset} Insufficient order book depth for {side} order of size {position_size}")
                            return False, 0.0
                            
                        # Calculate limit price (starting at mid-price)
                        mid_price = (asset_data["hl_best_bid"] + asset_data["hl_best_ask"]) / 2
                        
                        # Adjust towards more aggressive price on retry
                        # Start at mid-price, then move towards bid/ask
                        if attempt == 0:
                            # First attempt - use mid price with slippage
                            if is_entry:
                                # Selling, so use mid price with small discount
                                limit_price = mid_price * (1 - slippage_factor)
                            else:
                                # Buying, so use mid price with small premium
                                limit_price = mid_price * (1 + slippage_factor)
                        else:
                            # Subsequent attempts - move closer to bid/ask
                            if is_entry:
                                # Selling, so move closer to bid (lower)
                                adjustment = (mid_price - asset_data["hl_best_bid"]) * (attempt / max_retries)
                                limit_price = mid_price - adjustment
                            else:
                                # Buying, so move closer to ask (higher)
                                adjustment = (asset_data["hl_best_ask"] - mid_price) * (attempt / max_retries)
                                limit_price = mid_price + adjustment
                                
                        # Round to appropriate precision
                        limit_price = round(limit_price, asset_data["price_precision"])
                        
                        self.logger.info(f"{asset} Placing Hyperliquid {side} LIMIT order: Size={position_size} at ${limit_price}")
                        order_response = self.hl_exchange.order(
                            asset,
                            not is_entry,  # is_buy (False for entry/sell, True for exit/buy)
                            position_size,
                            limit_price,
                            {"limit": {"tif": "Gtc"}}  # Good-till-cancelled limit order
                        )
                        
                        # Check response
                        if order_response and 'status' in order_response and order_response['status'] == 'success':
                            # Extract order ID from the response
                            order_info = order_response.get('data', {}).get('orderInfo', {})
                            asset_data["current_hl_order_id"] = order_info.get('orderId')
                            
                            self.logger.info(f"{asset} Placed Hyperliquid {side} order: Size={position_size} at ${limit_price}")
                            
                            # Wait for fill
                            fill_status, filled_size = self.wait_for_hl_fill(asset)
                            
                            if fill_status:
                                # Verify position after fill
                                actual_size = self.verify_hl_position(asset, is_entry)
                                
                                if actual_size is not None:
                                    return True, actual_size
                            else:
                                # Cancel if not filled
                                self.cancel_hl_order(asset)
                                
                                # Check if we need to retry with more aggressive price
                                if attempt < max_retries - 1:
                                    self.logger.info(f"{asset} Order not filled, retrying with more aggressive price...")
                                    time.sleep(1)
                        else:
                            self.logger.error(f"{asset} Error placing HL limit order: {order_response}")
                except Exception as e:
                    self.logger.error(f"Error placing Hyperliquid order for {asset} (attempt {attempt+1}): {e}")
                    if attempt < max_retries - 1:
                        time.sleep(1)
                        
            return False, 0.0
            
        except Exception as e:
            self.logger.error(f"Error in Hyperliquid order placement for {asset}: {e}")
            return False, 0.0
    
    def verify_hl_position(self, asset: str, is_entry: bool) -> Optional[float]:
        """
        Verify Hyperliquid position was created with expected size
        
        Args:
            asset: Asset symbol
            is_entry: True for entry (short), False for exit (flat)
            
        Returns:
            Actual position size if successful, None if verification failed
        """
        try:
            # Get current positions
            position_size = self.get_hl_position_size(asset)
            
            if position_size is None:
                self.logger.error(f"Failed to retrieve Hyperliquid position for {asset}")
                return None
                
            if is_entry and position_size < 0:
                # Short position (negative size)
                self.logger.info(f"Verified {asset} HL short position: {abs(position_size)}")
                return abs(position_size)
            elif not is_entry and abs(position_size) < 0.001:
                # Flat position (zero or very small)
                self.logger.info(f"Verified {asset} HL position closed")
                return 0.0
                
            # Position not found or incorrect direction
            if is_entry:
                self.logger.error(f"Failed to verify HL short position for {asset}")
            else:
                self.logger.error(f"Failed to verify HL position closure for {asset}")
                
            return None
            
        except Exception as e:
            self.logger.error(f"Error verifying HL position for {asset}: {e}")
            return None
    
    def place_kraken_order(self, asset: str, is_entry: bool, position_size: Optional[float] = None) -> Tuple[bool, float]:
        """
        Place order on Kraken with rate limiting
        
        Args:
            asset: Asset symbol
            is_entry: True for entry (buy), False for exit (sell)
            position_size: Optional size override, uses calculated size if None
            
        Returns:
            Tuple of (success status, order size)
        """
        try:
            asset_data = self.assets[asset]
            side = "buy" if is_entry else "sell"
            
            self.update_kraken_prices(asset)
            
            if not all([asset_data["kraken_best_bid"], asset_data["kraken_best_ask"]]):
                self.logger.error(f"{asset} No valid prices available for Kraken order")
                return False, 0.0
                
            # FIX #2: Dynamic slippage based on volatility
            slippage_factor = self.get_recent_volatility(asset)
            self.logger.info(f"{asset} Using dynamic slippage factor for Kraken: {slippage_factor:.4f}%")
            
            # Determine volume to trade
            if position_size is not None:
                # Use provided position size
                volume = position_size
            else:
                # Calculate size for entry
                if is_entry:
                    volume = self.calculate_position_size(
                        asset, asset_data["kraken_best_ask"] * (1 + slippage_factor)
                    )
                else:
                    # Use actual position size for exit
                    volume = asset_data["kraken_position_size"]
                    
            # Ensure volume is valid
            if volume <= 0:
                self.logger.error(f"{asset} Invalid Kraken order volume: {volume}")
                return False, 0.0
                
            # Set price with slippage
            if is_entry:
                # Buying, so use ask with premium
                price = asset_data["kraken_best_ask"] * (1 + slippage_factor)
            else:
                # Selling, so use bid with discount
                price = asset_data["kraken_best_bid"] * (1 - slippage_factor)
                
            # Format price and volume based on asset precision
            if asset == "BTC":
                price_str = str(round(price, 1))  # Format price to 1 decimal place for BTC/USD
                volume_str = str(round(volume, 8))  # Format volume to 8 decimal places for BTC
            else:
                price_str = str(round(price, 2))  # Format price to 2 decimal places for other assets
                volume_str = str(round(volume, 6))  # Format volume to 6 decimal places for other assets
                
            self.logger.info(f"{asset} Placing Kraken {side} order: {volume_str} at ${price_str}")
            
            for attempt in range(self.max_retries):
                try:
                    # Place limit order
                    order_data = {
                        "nonce": str(int(1000*time.time())),
                        "ordertype": "limit",
                        "type": side,
                        "volume": volume_str,
                        "pair": asset_data["kraken_pair"],
                        "price": price_str
                    }
                    
                    result = self.kraken_request('/0/private/AddOrder', order_data)
                    
                    if result.get('error'):
                        self.logger.error(f"{asset} Kraken order error: {result['error']}")
                        
                        if attempt < self.max_retries - 1:
                            time.sleep(2)  # Wait longer between retries
                            
                            # Update prices and adjust price for next attempt
                            self.update_kraken_prices(asset)
                            
                            # Make more aggressive price adjustments on retry
                            if is_entry:
                                # For buy orders, increase price to improve fill probability
                                adjustment = (asset_data["kraken_best_ask"] - price) * (attempt + 1) / self.max_retries
                                price = price + adjustment
                            else:
                                # For sell orders, decrease price to improve fill probability
                                adjustment = (price - asset_data["kraken_best_bid"]) * (attempt + 1) / self.max_retries
                                price = price - adjustment
                                
                            # Format price based on asset precision
                            if asset == "BTC":
                                price_str = str(round(price, 1))
                            else:
                                price_str = str(round(price, 2))
                                
                            continue
                            
                    if 'result' in result and 'txid' in result['result']:
                        asset_data["current_kraken_order_id"] = result['result']['txid'][0]
                        self.logger.info(f"{asset} Kraken order placed: {side} {volume_str} at ${price_str}")
                        
                        # Wait for fill
                        fill_status, filled_volume = self.wait_for_kraken_fill(asset)
                        
                        if fill_status and filled_volume > 0:
                            # FIX #1: Return actual filled volume, not requested volume
                            return True, filled_volume
                        else:
                            # Cancel if not filled
                            self.cancel_kraken_order(asset)
                except Exception as e:
                    self.logger.error(f"Error placing Kraken order for {asset} (attempt {attempt+1}): {e}")
                    
                    if attempt < self.max_retries - 1:
                        time.sleep(2)  # Wait longer between retries
                        
            return False, 0.0
            
        except Exception as e:
            self.logger.error(f"Error in Kraken order placement for {asset}: {e}")
            return False, 0.0
    
    def wait_for_kraken_fill(self, asset: str) -> Tuple[bool, float]:
        """
        Wait for Kraken order to fill with rate limited checks
        
        Args:
            asset: Asset symbol
            
        Returns:
            Tuple of (fill status, filled volume)
        """
        asset_data = self.assets[asset]
        start_time = time.time()
        last_check_time = 0
        
        while time.time() - start_time < self.order_timeout:
            try:
                # Only check at the specified interval to avoid rate limits
                current_time = time.time()
                if current_time - last_check_time < self.kraken_order_check_interval:
                    time.sleep(0.5)  # Small sleep to prevent tight loop
                    continue
                    
                last_check_time = current_time
                
                fill_info = self.get_kraken_order_fill_info(asset)
                
                if not fill_info:
                    time.sleep(self.kraken_order_check_interval)
                    continue
                    
                status = fill_info.get('status')
                filled_vol = float(fill_info.get('vol_exec', 0))
                fill_percent = fill_info.get('fill_percent', 0)
                
                # Log progress for partial fills
                if fill_percent > 0 and fill_percent < 100:
                    self.logger.info(f"{asset} Kraken order {fill_percent:.1f}% filled ({filled_vol} / {fill_info.get('vol', 0)})")
                    
                if status == 'closed':
                    self.logger.info(f"{asset} Kraken order filled: {filled_vol}")
                    return True, filled_vol
                    
                time.sleep(self.kraken_order_check_interval)
                
            except Exception as e:
                if 'Rate limit exceeded' in str(e):
                    self.logger.warning(f"{asset} Rate limit hit during order check, waiting longer...")
                    time.sleep(5)  # Wait longer on rate limit errors
                else:
                    self.logger.error(f"Error checking Kraken order status for {asset}: {e}")
                
                time.sleep(self.kraken_order_check_interval)
                
        self.logger.warning(f"{asset} Kraken order timeout after {self.order_timeout} seconds")
        
        # Check one final time to see if it filled
        try:
            fill_info = self.get_kraken_order_fill_info(asset)
            if fill_info and fill_info.get('status') == 'closed':
                filled_vol = float(fill_info.get('vol_exec', 0))
                self.logger.info(f"{asset} Kraken order filled after timeout: {filled_vol}")
                return True, filled_vol
        except Exception:
            pass
            
        return False, 0.0
    
    def get_kraken_order_fill_info(self, asset: str) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive Kraken order fill information with rate limiting
        
        Args:
            asset: Asset symbol
            
        Returns:
            Dict with order details or None if error
        """
        try:
            asset_data = self.assets[asset]
            
            if not asset_data["current_kraken_order_id"]:
                return None
                
            # Enforce rate limit
            self.enforce_kraken_rate_limit()
            
            data = {
                "nonce": str(int(1000*time.time())),
                "txid": asset_data["current_kraken_order_id"]
            }
            
            result = self.kraken_request('/0/private/QueryOrders', data)
            
            if result.get('error'):
                self.logger.error(f"Error querying Kraken order for {asset}: {result['error']}")
                return None
                
            if 'result' in result and asset_data["current_kraken_order_id"] in result['result']:
                order = result['result'][asset_data["current_kraken_order_id"]]
                
                vol = float(order.get('vol', 0))
                vol_exec = float(order.get('vol_exec', 0))
                
                return {
                    'status': order.get('status'),
                    'vol': vol,
                    'vol_exec': vol_exec,
                    'fill_percent': (vol_exec / vol * 100) if vol > 0 else 0,
                    'price': float(order.get('price', 0))
                }
                
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting Kraken order fill info for {asset}: {e}")
            return None
    
    def wait_for_hl_fill(self, asset: str) -> Tuple[bool, float]:
        """
        Wait for Hyperliquid order to fill with detailed status tracking
        
        Args:
            asset: Asset symbol
            
        Returns:
            Tuple of (fill status, filled size)
        """
        asset_data = self.assets[asset]
        start_time = time.time()
        last_check_time = 0
        
        # Use a slightly faster check interval for Hyperliquid since it doesn't have the same rate limits
        hl_check_interval = 1.5  # 1.5 seconds between checks
        
        while time.time() - start_time < self.order_timeout:
            try:
                # Only check at the specified interval to avoid excessive API calls
                current_time = time.time()
                if current_time - last_check_time < hl_check_interval:
                    time.sleep(0.5)  # Small sleep to prevent tight loop
                    continue
                    
                last_check_time = current_time
                
                if not asset_data["current_hl_order_id"]:
                    return False, 0.0
                    
                # Get order status
                order_status = self.hl_exchange.get_order_status(asset_data["current_hl_order_id"])
                
                if not order_status:
                    time.sleep(hl_check_interval)
                    continue
                    
                status = order_status.get('status')
                filled = float(order_status.get('filled', 0))
                size = float(order_status.get('size', 1))  # Default to 1 to avoid division by zero
                fill_percent = (filled / size) * 100 if size else 0
                
                # Check if order is filled
                if status == 'filled':
                    self.logger.info(f"{asset} Hyperliquid order filled: {filled}")
                    return True, filled
                    
                # If order is partially filled, log progress
                if status == 'open' and fill_percent > 0:
                    self.logger.info(f"{asset} Hyperliquid order {fill_percent:.1f}% filled ({filled}/{size})")
                    
                time.sleep(hl_check_interval)
                
            except Exception as e:
                self.logger.error(f"Error checking Hyperliquid order status for {asset}: {e}")
                time.sleep(hl_check_interval)
                
        self.logger.warning(f"{asset} Hyperliquid order timeout after {self.order_timeout} seconds")
        
        # Check one final time to see if it filled
        try:
            order_status = self.hl_exchange.get_order_status(asset_data["current_hl_order_id"])
            if order_status and order_status.get('status') == 'filled':
                filled = float(order_status.get('filled', 0))
                self.logger.info(f"{asset} Hyperliquid order filled after timeout: {filled}")
                return True, filled
        except Exception:
            pass
            
        return False, 0.0
    
    def cancel_hl_order(self, asset: str) -> bool:
        """
        Cancel Hyperliquid order
        
        Args:
            asset: Asset symbol
            
        Returns:
            True if successful, False otherwise
        """
        try:
            asset_data = self.assets[asset]
            
            if not asset_data["current_hl_order_id"]:
                return False
                
            cancel_response = self.hl_exchange.cancel_order(asset_data["current_hl_order_id"])
            
            if cancel_response and cancel_response.get('status') == 'success':
                self.logger.info(f"{asset} Cancelled Hyperliquid order {asset_data['current_hl_order_id']}")
                asset_data["current_hl_order_id"] = None
                return True
            else:
                self.logger.error(f"{asset} Failed to cancel Hyperliquid order: {cancel_response}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error cancelling Hyperliquid order for {asset}: {e}")
            return False
    
    def cancel_kraken_order(self, asset: str) -> bool:
        """
        Cancel Kraken order with rate limiting
        
        Args:
            asset: Asset symbol
            
        Returns:
            True if successful, False otherwise
        """
        try:
            asset_data = self.assets[asset]
            
            if not asset_data["current_kraken_order_id"]:
                return False
                
            # Enforce rate limit
            self.enforce_kraken_rate_limit()
            
            data = {
                "nonce": str(int(1000*time.time())),
                "txid": asset_data["current_kraken_order_id"]
            }
            
            result = self.kraken_request('/0/private/CancelOrder', data)
            
            if not result.get('error'):
                self.logger.info(f"{asset} Cancelled Kraken order {asset_data['current_kraken_order_id']}")
                asset_data["current_kraken_order_id"] = None
                return True
            else:
                self.logger.error(f"{asset} Failed to cancel Kraken order: {result.get('error')}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error cancelling Kraken order for {asset}: {e}")
            return False
    
    def close_hl_position(self, asset: str) -> bool:
        """
        Emergency close Hyperliquid position
        
        Args:
            asset: Asset symbol
            
        Returns:
            True if successful, False otherwise
        """
        try:
            asset_data = self.assets[asset]
            
            # Cancel any open orders first
            if asset_data["current_hl_order_id"]:
                self.cancel_hl_order(asset)
                
            # Get current position size
            position_size = self.get_hl_position_size(asset)
            
            if position_size is None or abs(position_size) < 0.001:
                self.logger.info(f"{asset} No Hyperliquid position to close")
                return True
                
            # Place market order to close
            self.logger.info(f"{asset} Emergency closing Hyperliquid position of {abs(position_size)}")
            order_response = self.hl_exchange.order(
                asset,
                True,  # Buy to close short
                abs(position_size),
                None,  # Market order
                {"market": {}}  # Market order type
            )
            
            if order_response and order_response.get('status') == 'success':
                self.logger.info(f"{asset} Emergency closed Hyperliquid position")
                
                # Wait for confirmation
                time.sleep(2)
                
                # Verify position closed
                new_size = self.get_hl_position_size(asset)
                if new_size is None or abs(new_size) < 0.001:
                    return True
                else:
                    self.logger.error(f"{asset} Failed to close entire position, remaining: {new_size}")
                    return False
            else:
                self.logger.error(f"{asset} Failed to emergency close Hyperliquid position: {order_response}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error emergency closing Hyperliquid position for {asset}: {e}")
            return False
    
    def get_hl_position_size(self, asset: str) -> Optional[float]:
        """
        Get current Hyperliquid position size
        
        Args:
            asset: Asset symbol
            
        Returns:
            Position size (negative for short), None if error
        """
        try:
            # Call positions API endpoint
            positions = self.hl_exchange.positions()
            
            if not positions or 'positions' not in positions:
                self.logger.error(f"Failed to retrieve Hyperliquid positions for {asset}")
                return None
                
            # Find position for our asset
            for position in positions.get('positions', []):
                if position.get('coin') == asset:
                    size_value = position.get('szi', 0)
                    
                    # Convert size to float - negative for short position
                    if isinstance(size_value, str):
                        size = float(size_value)
                    else:
                        size = float(size_value)
                        
                    return size
                    
            # No position found
            return 0.0
            
        except Exception as e:
            self.logger.error(f"Error getting HL position size for {asset}: {e}")
            return None
    
    def synchronize_positions(self, asset: str) -> bool:
        """
        Make sure positions on both exchanges match to avoid exposure
        
        Args:
            asset: Asset symbol
            
        Returns:
            True if positions are synchronized, False otherwise
        """
        try:
            asset_data = self.assets[asset]
            
            # Get current positions
            hl_size = self.get_hl_position_size(asset)
            
            if hl_size is None:
                self.logger.error(f"Unable to determine Hyperliquid position size for {asset}")
                return False
                
            # Get Kraken position size
            kraken_size = asset_data["kraken_position_size"]
            
            if abs(hl_size) < 0.001 and abs(kraken_size) < 0.001:
                # Both positions are effectively zero
                return True
                
            if abs(abs(hl_size) - kraken_size) < 0.001:
                # Positions match (accounting for negative sign on HL shorts)
                return True
                
            self.logger.warning(f"{asset} Position mismatch detected: HL={hl_size}, Kraken={kraken_size}")
            
            # If we have a Hyperliquid position but no Kraken, close Hyperliquid
            if abs(hl_size) > 0.001 and abs(kraken_size) < 0.001:
                self.logger.warning(f"{asset} Closing orphaned Hyperliquid position")
                return self.close_hl_position(asset)
                
            # If we have a Kraken position but no Hyperliquid, sell it
            if abs(kraken_size) > 0.001 and abs(hl_size) < 0.001:
                self.logger.warning(f"{asset} Closing orphaned Kraken position")
                success, _ = self.place_kraken_order(
                    asset=asset,
                    is_entry=False,
                    position_size=kraken_size
                )
                return success
                
            # If both positions exist but don't match, adjust the smaller one
            if abs(hl_size) > kraken_size:
                # Adjust Hyperliquid down to match Kraken
                diff = abs(hl_size) - kraken_size
                self.logger.warning(f"{asset} Reducing Hyperliquid position by {diff}")
                
                # Place a buy order for the difference to reduce short position
                order_response = self.hl_exchange.order(
                    asset,
                    True,  # Buy to reduce short
                    diff,
                    None,  # Market order
                    {"market": {}}
                )
                
                return order_response and order_response.get('status') == 'success'
            else:
                # Adjust Kraken down to match Hyperliquid
                diff = kraken_size - abs(hl_size)
                self.logger.warning(f"{asset} Reducing Kraken position by {diff}")
                
                success, _ = self.place_kraken_order(
                    asset=asset,
                    is_entry=False,
                    position_size=diff
                )
                
                return success
                
        except Exception as e:
            self.logger.error(f"Error synchronizing positions for {asset}: {e}")
            return False
    
    def run(self):
        """Main bot loop"""
        self.logger.info("Starting arbitrage bot...")
        
        # Initial setup
        self.connect_websocket()
        time.sleep(5)  # Wait for initial connection and data
        
        try:
            while self.running:
                try:
                    # Use execute_with_cooldown for error handling (Fix #5)
                    self.execute_with_cooldown(self.check_conditions)
                    
                    # Update market data periodically for all assets
                    for asset in self.assets:
                        self.execute_with_cooldown(self.update_kraken_prices, asset)
                        
                    # Periodically check if positions are synchronized - but at a slow rate to avoid API limits
                    current_time = time.time()
                    for asset in self.assets:
                        asset_data = self.assets[asset]
                        if asset_data["in_position"] and current_time % 600 < 1:  # Every ~10 minutes
                            self.execute_with_cooldown(self.synchronize_positions, asset)
                            
                    # Log current state periodically
                    if current_time - self.last_prediction_check_time >= 30:  # Log every 30 seconds
                        self.last_prediction_check_time = current_time
                        current_dt = datetime.now(self.est_tz)
                        self.logger.info(f"Current Time: {current_dt.strftime('%Y-%m-%d %H:%M:%S')} EST")
                        
                        for asset in self.assets:
                            asset_data = self.assets[asset]
                            if asset_data["ws_funding_rate"] is not None:
                                current_rate = asset_data["ws_funding_rate"] * 100
                                self.logger.info(f"{asset} Current Funding Rate: {current_rate:.4f}%")
                                
                            if asset_data["in_position"]:
                                self.logger.info(f"{asset} In Position: HL={asset_data['hl_position_size']}, Kraken={asset_data['kraken_position_size']}")
                                
                            if asset_data["ws_predicted_rate"]:
                                predicted_rate = asset_data["ws_predicted_rate"] * 100
                                self.logger.info(f"{asset} Predicted Rate: {predicted_rate:.4f}%")
                                
                            # Check minute for timing reference
                            current_minute = datetime.now().minute
                            self.logger.info(f"{asset} Current minute: {current_minute} (Exit threshold: {60 - self.exit_time_threshold})")
                            
                    # Sleep to prevent CPU spinning
                    time.sleep(1)
                    
                except Exception as e:
                    self.logger.error(f"Error in main loop: {e}")
                    time.sleep(self.error_cooldown)
                    
        except KeyboardInterrupt:
            self.logger.info("Shutting down bot...")
            self.running = False
            
            # Exit all positions
            for asset in self.assets:
                asset_data = self.assets[asset]
                if asset_data["in_position"]:
                    self.logger.warning(f"{asset} Bot shutdown requested while in position!")
                    self.exit_positions(asset)
                    
        finally:
            if self.ws:
                self.ws.close()
                
            self.logger.info("Bot shutdown complete")


class Tier1Bot(ArbBotBase):
    """Tier 1 bot - Single asset arbitrage"""
    
    def __init__(self, config_path=None, user_id=None):
        super().__init__(config_path, user_id)
        
        # By default, support all available tokens
        self.supported_assets = ["HPOS", "BTC", "ETH", "BADGER", "HYPE"]
        
        # Set up asset configuration for all tokens
        self.assets = {
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
            "BTC": {
                "position_size": 12.0,  # Total position size in USD
                "margin_size": 4.0,  # Approximate margin required
                "hl_order_type": "limit",  # Use limit orders on Hyperliquid for BTC
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
                "kraken_pair": "XXBTZUSD",  # Kraken pair for BTC
                "price_precision": 1,  # Price precision for orders
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
                "price_precision": 4,  #
             },
            "HYPE": {
                "position_size": 12.0,  # Total position size in USD
                "margin_size": 4.0,  # Approximate margin required
                "hl_order_type": "limit",  # Use limit orders on Hyperliquid for HYPE
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
                "kraken_pair": None,  # Special case: both spot and perp on Hyperliquid
                "hyperliquid_spot": True,  # Flag indicating spot is on Hyperliquid
                "price_precision": 4,  # Price precision for orders
            }
        }
        
        # Initialize
        self.initialize()


class Tier2Bot(ArbBotBase):
    """Tier 2 bot - Two asset arbitrage"""
    
    def __init__(self, config_path=None, user_id=None):
        super().__init__(config_path, user_id)
        
        # By default, support all available tokens
        self.supported_assets = ["HPOS", "BTC", "ETH", "BADGER", "HYPE"]
        
        # Set up asset configuration for all tokens - identical to Tier1Bot
        # This is fine since we'll filter by selected_tokens in initialize()
        self.assets = {
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
            "BTC": {
                "position_size": 12.0,  # Total position size in USD
                "margin_size": 4.0,  # Approximate margin required
                "hl_order_type": "limit",  # Use limit orders on Hyperliquid for BTC
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
                "kraken_pair": "XXBTZUSD",  # Kraken pair for BTC
                "price_precision": 1,  # Price precision for orders
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
            "HYPE": {
                "position_size": 12.0,  # Total position size in USD
                "margin_size": 4.0,  # Approximate margin required
                "hl_order_type": "limit",  # Use limit orders on Hyperliquid for HYPE
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
                "kraken_pair": None,  # Special case: both spot and perp on Hyperliquid
                "hyperliquid_spot": True,  # Flag indicating spot is on Hyperliquid
                "price_precision": 4,  # Price precision for orders
            }
        }
        
        # Initialize
        self.initialize()


class Tier3Bot(ArbBotBase):
    """Tier 3 bot - Multi-asset arbitrage (all tokens)"""
    
    def __init__(self, config_path=None, user_id=None):
        super().__init__(config_path, user_id)
        
        # Set up base assets - identical to Tier1Bot and Tier2Bot
        self.supported_assets = ["HPOS", "BTC", "ETH", "BADGER", "HYPE"]
        
        # Set up base asset configurations
        self.assets = {
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
            "BTC": {
                "position_size": 12.0,  # Total position size in USD
                "margin_size": 4.0,  # Approximate margin required
                "hl_order_type": "limit",  # Use limit orders on Hyperliquid for BTC
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
                "kraken_pair": "XXBTZUSD",  # Kraken pair for BTC
                "price_precision": 1,  # Price precision for orders
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
            "HYPE": {
                "position_size": 12.0,  # Total position size in USD
                "margin_size": 4.0,  # Approximate margin required
                "hl_order_type": "limit",  # Use limit orders on Hyperliquid for HYPE
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
                "kraken_pair": None,  # Special case: both spot and perp on Hyperliquid
                "hyperliquid_spot": True,  # Flag indicating spot is on Hyperliquid
                "price_precision": 4,  # Price precision for orders
            }
        }
        
        # Initialize
        self.initialize()
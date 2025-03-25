#!/usr/bin/env python3
"""
Bot Service Module for Abraxas Greenprint Funding Bot
------------------------------------------
Manages bot instances for multiple users
"""

import os
import logging
import configparser
import threading
import json
from datetime import datetime
from typing import Dict, Any, Optional, List

from arb_bot import Tier1Bot, Tier2Bot, Tier3Bot

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class BotService:
    """Service to manage bot instances for multiple users"""
    
    def __init__(self, config_dir: str = "/opt/crypto-arb-bot/config"):
        """
        Initialize bot service
        
        Args:
            config_dir: Directory to store configuration files
        """
        self.config_dir = config_dir
        self.bots = {}  # Store running bot instances
        self.ensure_config_dir()
        
    def ensure_config_dir(self):
        """Ensure configuration directory exists with proper permissions"""
        if not os.path.exists(self.config_dir):
            try:
                # Create directory with restricted permissions (only readable by owner)
                os.makedirs(self.config_dir, mode=0o700, exist_ok=True)
                logger.info(f"Created config directory: {self.config_dir}")
            except Exception as e:
                logger.error(f"Failed to create config directory: {str(e)}")
                # Fall back to temporary directory if main directory creation fails
                self.config_dir = "/tmp/arb_bot"
                os.makedirs(self.config_dir, mode=0o700, exist_ok=True)
                logger.warning(f"Using fallback config directory: {self.config_dir}")
        
    def create_config(self, user_id: str, tier: int, kraken_key: str, 
                    kraken_secret: str, hl_key: str, hl_secret: str,
                    selected_tokens: List[str] = None) -> str:
        """
        Create configuration file for user
        
        Args:
            user_id: User's telegram ID
            tier: Subscription tier
            kraken_key: Kraken API key
            kraken_secret: Kraken API secret
            hl_key: Hyperliquid API key
            hl_secret: Hyperliquid private key
            selected_tokens: List of token symbols to trade
            
        Returns:
            Path to created config file
        """
        try:
            # Create config parser
            config = configparser.ConfigParser()
            
            # Add API credentials
            config['kraken'] = {
                'api_key': kraken_key,
                'api_secret': kraken_secret
            }
            
            config['hyperliquid'] = {
                'api_key': hl_key,
                'private_key': hl_secret
            }
            
            # Add service configuration
            config['service'] = {
                'tier': str(tier),
                'user_id': user_id,
                'max_slippage': '0.05',  # 5% max slippage (flash crash protection)
                'liquidation_threshold': '0.2'  # 20% margin threshold
            }
            
            # Add selected tokens if provided
            if selected_tokens:
                config['tokens'] = {
                    'selected': ','.join(selected_tokens)
                }
            
            # Determine config file path (named with user ID)
            config_path = os.path.join(self.config_dir, f"{user_id}.ini")
            
            # Write config with restricted permissions
            with open(config_path, 'w') as f:
                config.write(f)
                
            # Set secure permissions (only readable by owner)
            os.chmod(config_path, 0o600)
            
            return config_path
            
        except Exception as e:
            logger.error(f"Failed to create config for user {user_id}: {str(e)}")
            raise
            
    def start_bot(self, user_id: str, tier: int, kraken_key: str, 
                 kraken_secret: str, hl_key: str, hl_secret: str,
                 selected_tokens: List[str] = None) -> bool:
        """
        Start a bot for the user with the specified tier and tokens
        
        Args:
            user_id: User's telegram ID
            tier: Subscription tier
            kraken_key: Kraken API key
            kraken_secret: Kraken API secret
            hl_key: Hyperliquid API key
            hl_secret: Hyperliquid private key
            selected_tokens: List of token symbols to trade
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate tokens
            if not selected_tokens:
                logger.error(f"No tokens selected for user {user_id}")
                return False
                
            # Create config file
            config_path = self.create_config(
                user_id, tier, kraken_key, kraken_secret, hl_key, hl_secret,
                selected_tokens=selected_tokens
            )
            
            # Stop existing bot if running
            self.stop_bot(user_id)
            
            # Create appropriate bot based on tier
            if tier == 1:
                bot = Tier1Bot(config_path, user_id)
            elif tier == 2:
                bot = Tier2Bot(config_path, user_id)
            elif tier == 3:
                bot = Tier3Bot(config_path, user_id)
            else:
                logger.error(f"Invalid tier: {tier}")
                return False
                
            # Start bot in separate thread
            bot_thread = threading.Thread(target=bot.run)
            bot_thread.daemon = True
            bot_thread.start()
            
            # Store bot instance
            self.bots[user_id] = {
                'bot': bot,
                'thread': bot_thread,
                'tier': tier,
                'config_path': config_path,
                'start_time': datetime.now(),
                'selected_tokens': selected_tokens
            }
            
            logger.info(f"Started tier {tier} bot for user {user_id} with tokens: {', '.join(selected_tokens)}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start bot for user {user_id}: {str(e)}")
            return False
            
    def stop_bot(self, user_id: str) -> bool:
        """
        Stop bot for the specified user
        
        Args:
            user_id: User's telegram ID
            
        Returns:
            True if successful, False otherwise
        """
        if user_id in self.bots:
            try:
                bot_info = self.bots[user_id]
                bot = bot_info['bot']
                
                # Signal bot to stop
                logger.info(f"Stopping bot for user {user_id}")
                bot.running = False
                
                # Wait for bot to exit positions and clean up (max 60 seconds)
                bot_info['thread'].join(timeout=60)
                
                # Remove config file
                if os.path.exists(bot_info['config_path']):
                    os.remove(bot_info['config_path'])
                    
                # Remove bot from list
                del self.bots[user_id]
                logger.info(f"Bot stopped for user {user_id}")
                return True
                
            except Exception as e:
                logger.error(f"Error stopping bot for user {user_id}: {str(e)}")
                # Try to clean up even if error occurred
                if user_id in self.bots:
                    del self.bots[user_id]
                return False
                
        logger.info(f"No bot running for user {user_id}")
        return True
        
    def get_bot_status(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get status of bot for the specified user
        
        Args:
            user_id: User's telegram ID
            
        Returns:
            Dict with bot status or None if not found
        """
        if user_id in self.bots:
            try:
                bot_info = self.bots[user_id]
                bot = bot_info['bot']
                
                # Collect status information
                status = {
                    'tier': bot_info['tier'],
                    'running': bot.running,
                    'start_time': bot_info['start_time'],
                    'uptime': (datetime.now() - bot_info['start_time']).total_seconds(),
                    'positions': {},
                    'selected_tokens': bot_info.get('selected_tokens', [])
                }
                
                # Collect position information
                for asset in bot.assets:
                    asset_data = bot.assets[asset]
                    if asset_data["in_position"]:
                        status['positions'][asset] = {
                            'hl_position': asset_data["hl_position_size"],
                            'kraken_position': asset_data["kraken_position_size"],
                            'entry_time': asset_data.get("entry_time", None)
                        }
                        
                return status
                
            except Exception as e:
                logger.error(f"Error getting bot status for user {user_id}: {str(e)}")
                
        return None
        
    def list_active_bots(self) -> Dict[str, Dict[str, Any]]:
        """
        List all active bots
        
        Returns:
            Dict mapping user IDs to bot info
        """
        active_bots = {}
        
        for user_id, info in self.bots.items():
            try:
                active_bots[user_id] = {
                    'tier': info['tier'],
                    'start_time': info['start_time'],
                    'uptime': (datetime.now() - info['start_time']).total_seconds(),
                    'is_running': info['bot'].running,
                    'selected_tokens': info.get('selected_tokens', [])
                }
            except Exception as e:
                logger.error(f"Error getting info for bot {user_id}: {str(e)}")
                
        return active_bots
        
    def update_bot_tokens(self, user_id: str, tokens: List[str]) -> bool:
        """
        Update tokens for a running bot
        
        Args:
            user_id: User's telegram ID
            tokens: New list of tokens to trade
            
        Returns:
            True if successful, False otherwise
        """
        if user_id not in self.bots:
            logger.error(f"No running bot found for user {user_id}")
            return False
            
        try:
            bot_info = self.bots[user_id]
            
            # Restart the bot with new tokens
            tier = bot_info['tier']
            config_path = bot_info['config_path']
            
            # Update config file
            config = configparser.ConfigParser()
            config.read(config_path)
            
            if 'tokens' not in config:
                config['tokens'] = {}
                
            config['tokens']['selected'] = ','.join(tokens)
            
            with open(config_path, 'w') as f:
                config.write(f)
                
            # We need to restart the bot to apply new tokens
            # This would be handled better in production with a dynamic update mechanism
            self.stop_bot(user_id)
            
            # Get API keys from config
            kraken_key = config['kraken']['api_key']
            kraken_secret = config['kraken']['api_secret']
            hl_key = config['hyperliquid']['api_key']
            hl_secret = config['hyperliquid']['private_key']
            
            # Start new bot with updated tokens
            self.start_bot(
                user_id=user_id,
                tier=tier,
                kraken_key=kraken_key,
                kraken_secret=kraken_secret,
                hl_key=hl_key,
                hl_secret=hl_secret,
                selected_tokens=tokens
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error updating tokens for user {user_id}: {str(e)}")
            return False
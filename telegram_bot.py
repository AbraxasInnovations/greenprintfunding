#!/usr/bin/env python3
"""
Abraxas Greenprint Funding Bot
-----------------------------
This bot allows users to subscribe to different tiers of funding arbitrage trading 
between Hyperliquid and Kraken exchanges, with customizable token selections.
"""

import os
import logging
import asyncio
import json
from datetime import datetime, timedelta
from typing import List, Dict, Set, Any
from telegram import (
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)
from telegram.constants import ParseMode
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    filters
)
from dotenv import load_dotenv
import time

from database import Database, User, APIKey, BotStatus, Transaction, TokenSelection
from security import SecurityManager
from bot_service import BotService
from payment import PaymentManager
from trading_pairs import (
    get_available_pairs, 
    get_available_pairs_list,
    format_pairs_description,
    validate_pair_selection,
    get_active_trading_pairs
)

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='/opt/crypto-arb-bot/logs/bot.log'
)
logger = logging.getLogger(__name__)

# Conversation states
(
    MAIN_MENU,
    AWAITING_TIER,
    AWAITING_TOKEN_SELECTION,
    AWAITING_PAYMENT_METHOD,
    AWAITING_KRAKEN_KEY,
    AWAITING_KRAKEN_SECRET,
    AWAITING_HL_KEY,
    AWAITING_HL_SECRET,
    AWAITING_HL_ADDRESS,  # New state for Hyperliquid address
    AWAITING_PAYMENT,
    CONFIRM_START,
    CONFIRM_STOP,
    CHOOSING_TIER,
    CHOOSING_TOKENS,
    CHOOSING_ENTRY_STRATEGY,
    CHOOSING_EXIT_STRATEGY,
    CONFIRMING_STRATEGIES,
    CHOOSING_PAYMENT,
    PAYMENT_EMAIL_ENTRY
) = range(19)  # Update range to include new state

class AbraxasGreenprintBot:
    """
    Telegram Bot for Abraxas Greenprint Funding Arbitrage
    """
    def __init__(self, token):
        self.token = token
        self.db = Database()
        self.security = SecurityManager()
        self.bot_service = BotService()
        self.payment = PaymentManager()
        self.logger = logger

        # Set pricing for each tier (USD)
        self.pricing = {
            1: 50,  # $50/month for Tier 1 (1 token)
            2: 100, # $100/month for Tier 2 (2 tokens)
            3: 200  # $200/month for Tier 3 (All tokens)
        }
        
        # Token limits per tier
        self.token_limits = {
            1: 1,  # Tier 1: 1 token
            2: 2,  # Tier 2: 2 tokens
            3: 99  # Tier 3: All tokens (setting a high limit)
        }
        
        # Cache available pairs
        self.available_pairs = get_active_trading_pairs()
        
        # Initialize telegram application
        self.application = Application.builder().token(token).build()
        self.setup_handlers()
        
    def setup_handlers(self):
        """Setup handlers for commands and callbacks"""
        logger.info("Setting up message handlers")
        
        # Define conversation states
        global CHOOSING_TIER, PAYMENT_EMAIL_ENTRY, CHOOSING_PAYMENT, AWAITING_PAYMENT_METHOD, AWAITING_PAYMENT
        global CHOOSING_TOKENS, CHOOSING_ENTRY_STRATEGY, CHOOSING_EXIT_STRATEGY, CONFIRMING_STRATEGIES
        global AWAITING_KRAKEN_KEY, AWAITING_KRAKEN_SECRET, AWAITING_HL_KEY, AWAITING_HL_SECRET
        
        # Add command handlers
        self.application.add_handler(CommandHandler("start", self.cmd_start))
        self.application.add_handler(CommandHandler("help", self.cmd_help))
        self.application.add_handler(CommandHandler("pairs", self.cmd_pairs))
        self.application.add_handler(CommandHandler("start_bot", self.cmd_start_bot))
        self.application.add_handler(CommandHandler("stop_bot", self.cmd_stop_bot))
        self.application.add_handler(CommandHandler("status", self.cmd_status))
        
        # Add subscription conversation handler
        subscribe_conv_handler = ConversationHandler(
            entry_points=[
                CommandHandler("subscribe", self.cmd_subscribe),
                CallbackQueryHandler(self.subscription_extend_callback, pattern="^subscribe_extend$"),
                CallbackQueryHandler(self.choose_tier_callback, pattern=r"^tier_\d$")
            ],
            states={
                CHOOSING_TIER: [
                    CallbackQueryHandler(self.choose_tier_callback, pattern=r"^tier_\d$")
                ],
                CHOOSING_TOKENS: [
                    CallbackQueryHandler(self.token_selection_callback, pattern=r'^(toggle_|save_tokens)')
                ],
                CHOOSING_ENTRY_STRATEGY: [
                    CallbackQueryHandler(self.entry_strategy_callback)
                ],
                CHOOSING_EXIT_STRATEGY: [
                    CallbackQueryHandler(self.exit_strategy_callback)
                ],
                CONFIRMING_STRATEGIES: [
                    CallbackQueryHandler(self.confirm_strategies_callback)
                ],
                CHOOSING_PAYMENT: [
                    CallbackQueryHandler(self.payment_method_callback)
                ],
                AWAITING_PAYMENT_METHOD: [
                    CallbackQueryHandler(self.payment_method_callback)
                ],
                AWAITING_PAYMENT: [
                    CallbackQueryHandler(self.payment_method_callback, pattern=r"^cancel_payment$")
                ],
                PAYMENT_EMAIL_ENTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.process_payment_email)]
            },
            fallbacks=[CommandHandler("cancel", self.cancel_conversation)]
        )
        self.application.add_handler(subscribe_conv_handler)
        
        # Remove the separate subscription extension handler since it's now part of the conversation
        # self.application.add_handler(CallbackQueryHandler(self.subscription_extend_callback, pattern="^subscribe_extend$"))
        self.application.add_handler(CallbackQueryHandler(self.cancel_callback, pattern="^cancel$"))
        
        # Add guided setup handlers - integrated with the strategy selection flow
        tokens_conv_handler = ConversationHandler(
            entry_points=[
                CallbackQueryHandler(self.guide_tokens_callback, pattern="^guide_tokens$"),
                CallbackQueryHandler(self.guide_strategies_callback, pattern="^guide_strategies$"),
                CommandHandler("tokens", self.cmd_tokens)
            ],
            states={
                CHOOSING_TOKENS: [
                    CallbackQueryHandler(self.manage_tokens_callback, pattern=r'^(toggle_|save_tokens)')
                ],
                CHOOSING_ENTRY_STRATEGY: [
                    CallbackQueryHandler(self.entry_strategy_callback)
                ],
                CHOOSING_EXIT_STRATEGY: [
                    CallbackQueryHandler(self.exit_strategy_callback)
                ],
                CONFIRMING_STRATEGIES: [
                    CallbackQueryHandler(self.confirm_strategies_callback)
                ]
            },
            fallbacks=[CommandHandler("cancel", self.cancel_conversation)]
        )
        self.application.add_handler(tokens_conv_handler)
        
        # Add callback query handlers for buttons
        self.application.add_handler(CallbackQueryHandler(self.confirm_start_callback, pattern="^confirm_start"))
        self.application.add_handler(CallbackQueryHandler(self.confirm_stop_callback, pattern="^confirm_stop"))
        
        # Add API key setup conversation handler
        logger.info("Setting up API key conversation handler")
        setkeys_conv_handler = ConversationHandler(
            entry_points=[
                CommandHandler("setkeys", self.cmd_setkeys),
                CallbackQueryHandler(self.guide_keys_callback, pattern="^guide_keys$")
            ],
            states={
                AWAITING_KRAKEN_KEY: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.process_kraken_key)],
                AWAITING_KRAKEN_SECRET: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.process_kraken_secret)],
                AWAITING_HL_KEY: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.process_hl_key)],
                AWAITING_HL_SECRET: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.process_hl_secret)],
                AWAITING_HL_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.process_hl_address)]
            },
            fallbacks=[CommandHandler("cancel", self.cancel_conversation)]
        )
        logger.info(f"API key conversation handler entry points: {[str(ep) for ep in setkeys_conv_handler.entry_points]}")
        logger.info(f"API key conversation handler states: {list(setkeys_conv_handler.states.keys())}")
        logger.info(f"API key conversation handler state handlers: {[(state, len(handlers)) for state, handlers in setkeys_conv_handler.states.items()]}")
        self.application.add_handler(setkeys_conv_handler)
    
        # Handle unknown commands LAST
        self.application.add_handler(MessageHandler(filters.COMMAND, self.unknown_command))
        
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command"""
        logger.info(f"Received /start command from user {update.effective_user.id}")
        user_id = update.effective_user.id
        username = update.effective_user.username or update.effective_user.first_name
        
        # Check if user exists in database
        user = self.db.get_user_by_telegram_id(user_id)
        if not user:
            self.db.create_user(telegram_id=user_id, username=username)
            welcome_text = (
                f"👋 *Welcome to the Abraxas Greenprint Funding Bot*, {username}!\n\n"
                "This bot allows you to run automated funding rate arbitrage trading "
                "between Hyperliquid and Kraken exchanges.\n\n"
                "Here's how to get started:\n"
                "1. /subscribe - Choose your subscription tier\n"
                "2. /tokens - Select which tokens to trade\n"
                "3. /setkeys - Configure your exchange API keys\n"
                "4. /start_bot - Start your trading bot\n\n"
                "Type /pairs to see available trading pairs.\n"
                "Type /help for more information."
            )
        else:
            welcome_text = (
                f"Welcome back to Abraxas Greenprint, {username}!\n\n"
                "What would you like to do?\n"
                "/subscribe - Manage your subscription\n"
                "/tokens - Select which tokens to trade\n"
                "/pairs - View available trading pairs\n"
                "/setkeys - Configure API keys\n"
                "/status - Check your bot status\n"
                "/start_bot - Start your bot\n"
                "/stop_bot - Stop your bot\n"
                "/help - Get help"
            )
            
        await update.message.reply_text(welcome_text)
        
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /help command"""
        logger.info(f"Received /help command from user {update.effective_user.id}")
        help_text = (
            "📚 *Abraxas Greenprint Funding Bot Help*\n\n"
            "*Available Commands:*\n"
            "/subscribe - Choose a subscription tier\n"
            "/tokens - Select which tokens to trade\n"
            "/pairs - View available trading pairs\n"
            "/setkeys - Configure exchange API keys\n"
            "/status - Check your bot status\n"
            "/start_bot - Start your trading bot\n"
            "/stop_bot - Stop your trading bot\n"
            "/help - Show this help message\n\n"
            
            "*Subscription Tiers:*\n"
            "🥉 *Tier 1* - $50/month - Trade 1 token of your choice\n"
            "🥈 *Tier 2* - $100/month - Trade 2 tokens of your choice\n"
            "🥇 *Tier 3* - $200/month - Trade all available tokens\n\n"
            
            "*How Funding Arbitrage Works:*\n"
            "The bot exploits the funding rate differences between perpetual futures "
            "and spot markets by:\n"
            "• Going short on perpetual futures on Hyperliquid\n"
            "• Going long on spot markets on Kraken (or Hyperliquid for HYPE)\n"
            "• Collecting the funding rate while maintaining delta neutrality\n\n"
            
            "*Security Information:*\n"
            "• Your API keys are encrypted using industry standard encryption\n"
            "• Private keys never leave our secure server\n"
            "• You can revoke access anytime by deleting your API keys\n\n"
            
            "*Need more help?*\n"
            "Contact @admin_username for support"
        )
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
        
    async def cmd_pairs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /pairs command to show available trading pairs"""
        # Refresh available pairs
        self.available_pairs = get_active_trading_pairs()
        
        # Format the pairs description
        pairs_text = format_pairs_description()
        
        await update.message.reply_text(pairs_text, parse_mode='Markdown')
        
    async def cmd_subscribe(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handles subscription command, prompting user to select a subscription tier"""
        user_id = update.effective_user.id
        
        # Check if user already has an active subscription
        user = self.db.get_user_by_telegram_id(user_id)
        
        if user and user.subscription_tier and user.subscription_expiry and user.subscription_expiry > datetime.now():
            remaining_days = (user.subscription_expiry - datetime.now()).days
            
            # User has an active subscription
            await update.message.reply_text(
                f"You already have an active Tier {user.subscription_tier} subscription "
                f"with {remaining_days} days remaining.\n\n"
                f"Would you like to extend your subscription?",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Yes, extend subscription", callback_data="subscribe_extend")],
                    [InlineKeyboardButton("No, cancel", callback_data="cancel")]
                ])
            )
            return ConversationHandler.END
        
        # User doesn't have an active subscription, show subscription options
        keyboard = [
            [InlineKeyboardButton(f"Tier 1: $50/month", callback_data="tier_1")],
            [InlineKeyboardButton(f"Tier 2: $100/month", callback_data="tier_2")],
            [InlineKeyboardButton(f"Tier 3: $200/month", callback_data="tier_3")]
        ]
        
        await update.message.reply_text(
            "Please select a subscription tier:\n\n"
            "🔹 *Tier 1* ($50/month):\n"
            "- Access to base funding bot features\n"
            "- 5 trading pairs\n"
            "- Basic risk management\n\n"
            
            "🔸 *Tier 2* ($100/month):\n"
            "- All Tier 1 features\n"
            "- 10 trading pairs\n"
            "- Enhanced risk management\n"
            "- Priority support\n\n"
            
            "💎 *Tier 3* ($200/month):\n"
            "- All Tier 2 features\n"
            "- Unlimited trading pairs\n"
            "- Advanced risk management\n"
            "- VIP support\n"
            "- Custom strategies",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        return CHOOSING_TIER
        
    async def choose_tier_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handles tier selection and presents payment options"""
        query = update.callback_query
        user_id = query.from_user.id
        
        await query.answer()
        
        if query.data.startswith("tier_"):
            tier = int(query.data.split("_")[1])
            context.user_data['selected_tier'] = tier
            
            # Store tier selection in context
            if 'payment_data' not in context.user_data:
                context.user_data['payment_data'] = {}
            
            context.user_data['payment_data']['tier'] = tier
            
            # Ask for email first before proceeding to payment methods
            await query.edit_message_text(
                f"You've selected Tier {tier}.\n\n"
                f"Before proceeding with payment, we need your email address to associate with your subscription.\n\n"
                f"Please enter your email address:"
            )
            
            return PAYMENT_EMAIL_ENTRY
        
        return ConversationHandler.END
        
    async def process_payment_email(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process the email address entered by the user"""
        user_id = update.effective_user.id
        email = update.message.text.strip()
        
        # Basic email validation
        import re
        email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if not email_pattern.match(email):
            await update.message.reply_text(
                "That doesn't look like a valid email address. Please enter a valid email:"
            )
            return PAYMENT_EMAIL_ENTRY
        
        # Store email in database
        if not self.db.update_user_email(user_id, email):
            # If user doesn't exist, create them first
            self.db.create_user(user_id, update.effective_user.username)
            self.db.update_user_email(user_id, email)
        
        # Store email in context for later use
        if 'payment_data' not in context.user_data:
            context.user_data['payment_data'] = {}
        context.user_data['payment_data']['email'] = email
        
        # Now show payment method options
        tier = context.user_data.get('selected_tier', 1)
        
        # Set the appropriate amount based on tier
        amount = 50  # Tier 1 default
        if tier == 2:
            amount = 100
        elif tier == 3:
            amount = 200
        
        context.user_data['payment_data']['amount'] = amount
        
        # Show payment options
        keyboard = [
            [InlineKeyboardButton("Pay with BoomFi (Crypto)", callback_data="pay_boomfi")]
        ]
        
        await update.message.reply_text(
            f"Thanks! We'll use {email} for your subscription.\n\n"
            f"You've selected Tier {tier} subscription: ${amount}/month.\n\n"
            f"Please choose your payment method:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        return CHOOSING_PAYMENT
        
    async def token_selection_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle token selection callback"""
        query = update.callback_query
        await query.answer()
        
        # For our updates from the cmd_tokens method, we should use manage_tokens_callback
        if query.data.startswith("toggle_") or query.data == "save_tokens":
            return await self.manage_tokens_callback(update, context)
            
        # Rest of the existing token_selection_callback implementation for subscription flow
        user_id = query.from_user.id
        selected_tier = context.user_data.get('selected_tier', 1)
        max_tokens = self.token_limits[selected_tier]
        
        if 'selected_tokens' not in context.user_data:
            context.user_data['selected_tokens'] = []
            
        if query.data == "tokens_done":
            # User is done selecting tokens
            if not context.user_data['selected_tokens']:
                # No tokens selected, ask user to select at least one
                await query.edit_message_text(
                    "Please select at least one token before proceeding.",
                    reply_markup=query.message.reply_markup
                )
                return CHOOSING_TOKENS
                
            # Format the selected tokens for display
            tokens_text = ", ".join(context.user_data['selected_tokens'])
            
            # Move to entry strategy selection instead of payment
            await query.edit_message_text(
                f"Great! You've selected: *{tokens_text}* for your Tier {selected_tier} subscription.\n\n"
                "Now, choose your *entry strategy*:",
                parse_mode='Markdown',
                reply_markup=self.get_entry_strategy_keyboard()
            )
            
            return CHOOSING_ENTRY_STRATEGY
            
        elif query.data.startswith("token_"):
            # User selected a token
            token = query.data.split("_")[1]
            
            # Check if token is already selected
            if token in context.user_data['selected_tokens']:
                # Remove token
                context.user_data['selected_tokens'].remove(token)
            else:
                # Check if max tokens reached
                if len(context.user_data['selected_tokens']) >= max_tokens:
                    await query.answer(f"Maximum {max_tokens} tokens for Tier {selected_tier}. Deselect a token first.")
                    return CHOOSING_TOKENS
                    
                # Add token
                context.user_data['selected_tokens'].append(token)
                
            # Update button appearance based on selection
            token_buttons = []
            for available_token in self.available_pairs:
                if available_token in context.user_data['selected_tokens']:
                    # Mark as selected
                    token_buttons.append([
                        InlineKeyboardButton(f"✅ {available_token}", callback_data=f"token_{available_token}")
                    ])
                else:
                    token_buttons.append([
                        InlineKeyboardButton(available_token, callback_data=f"token_{available_token}")
                    ])
                    
            token_buttons.append([
                InlineKeyboardButton("Done Selecting", callback_data="tokens_done")
            ])
            
            # Show current selections
            selected_text = ", ".join(context.user_data['selected_tokens']) if context.user_data['selected_tokens'] else "None"
            
            await query.edit_message_text(
                f"Tier {selected_tier} - ${self.pricing[selected_tier]}/month\n\n"
                f"This tier allows you to select up to {max_tokens} tokens.\n\n"
                f"*Currently selected*: {selected_text}\n"
                f"({len(context.user_data['selected_tokens'])}/{max_tokens})",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(token_buttons)
            )
            
            return CHOOSING_TOKENS
            
        # After token selection is complete, move to entry strategy selection
        if "done" in query.data:
            # Save selected tokens
            selected_tokens = context.user_data.get('selected_tokens', [])
            if not selected_tokens:
                await query.edit_message_text("You must select at least one token to continue. Please try again.")
                return ConversationHandler.END
                
            tier = context.user_data.get('selected_tier')
            
            # Display entry strategy selection
            await query.edit_message_text(
                f"Great! You've selected {', '.join(selected_tokens)} for your Tier {tier} subscription.\n\n"
                "Now, choose your *entry strategy*:",
                parse_mode="Markdown",
                reply_markup=self.get_entry_strategy_keyboard()
            )
            return CHOOSING_ENTRY_STRATEGY
        
    def get_entry_strategy_keyboard(self):
        """Create keyboard with entry strategy options"""
        keyboard = [
            [InlineKeyboardButton("Default Entry Strategy (enter above 60th percentile)", callback_data="entry_default")],
            [InlineKeyboardButton("Enter above 50th percentile", callback_data="entry_50")],
            [InlineKeyboardButton("Enter above 75th percentile", callback_data="entry_75")],
            [InlineKeyboardButton("Enter above 85th percentile", callback_data="entry_85")],
            [InlineKeyboardButton("Enter above 95th percentile", callback_data="entry_95")],
            [InlineKeyboardButton("Abraxas Optimized Funding", callback_data="entry_abraxas")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_exit_strategy_keyboard(self):
        """Create keyboard with exit strategy options"""
        keyboard = [
            [InlineKeyboardButton("Default Exit Strategy (sell before next negative rate)", callback_data="exit_default")],
            [InlineKeyboardButton("Exit below 50th percentile", callback_data="exit_50")],
            [InlineKeyboardButton("Exit below 35th percentile", callback_data="exit_35")],
            [InlineKeyboardButton("Exit below 20th percentile", callback_data="exit_20")],
            [InlineKeyboardButton("Exit below 10th percentile", callback_data="exit_10")],
            [InlineKeyboardButton("Abraxas Optimized Exit", callback_data="exit_abraxas")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_strategies_confirmation_keyboard(self):
        """Create keyboard for confirming strategy selections"""
        keyboard = [
            [InlineKeyboardButton("Confirm Strategies", callback_data="confirm_strategies")],
            [InlineKeyboardButton("Change Entry Strategy", callback_data="change_entry")],
            [InlineKeyboardButton("Change Exit Strategy", callback_data="change_exit")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    async def entry_strategy_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle entry strategy selection"""
        query = update.callback_query
        await query.answer()
        
        # Extract the selected entry strategy
        strategy_data = query.data
        
        # Map the callback data to descriptive text
        strategy_descriptions = {
            "entry_default": "Default (enter above 60th percentile)",
            "entry_50": "Enter above 50th percentile",
            "entry_75": "Enter above 75th percentile",
            "entry_85": "Enter above 85th percentile",
            "entry_95": "Enter above 95th percentile",
            "entry_abraxas": "Abraxas Optimized Funding (enter above 60th percentile)"
        }
        
        # Store the selected strategy
        context.user_data['entry_strategy'] = strategy_data.replace("entry_", "")
        context.user_data['entry_strategy_desc'] = strategy_descriptions.get(strategy_data)
        
        # Display exit strategy selection
        await query.edit_message_text(
            f"Entry strategy selected: *{strategy_descriptions.get(strategy_data)}*\n\n"
            "Now, choose your *exit strategy*:",
            parse_mode="Markdown",
            reply_markup=self.get_exit_strategy_keyboard()
        )
        return CHOOSING_EXIT_STRATEGY
    
    async def exit_strategy_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle exit strategy selection"""
        query = update.callback_query
        await query.answer()
        
        # Extract the selected exit strategy
        strategy_data = query.data
        
        # Map the callback data to descriptive text
        strategy_descriptions = {
            "exit_default": "Default (sell before next negative rate)",
            "exit_50": "Exit below 50th percentile",
            "exit_35": "Exit below 35th percentile",
            "exit_20": "Exit below 20th percentile",
            "exit_10": "Exit below 10th percentile",
            "exit_abraxas": "Abraxas Optimized Exit (sell before next negative rate)"
        }
        
        # Store the selected strategy
        context.user_data['exit_strategy'] = strategy_data.replace("exit_", "")
        context.user_data['exit_strategy_desc'] = strategy_descriptions.get(strategy_data)
        
        # Display confirmation of selected strategies
        entry_desc = context.user_data.get('entry_strategy_desc')
        exit_desc = strategy_descriptions.get(strategy_data)
        
        await query.edit_message_text(
            "*Strategy Selection Summary*\n\n"
            f"*Entry Strategy:* {entry_desc}\n"
            f"*Exit Strategy:* {exit_desc}\n\n"
            "Are you satisfied with these selections?",
            parse_mode="Markdown",
            reply_markup=self.get_strategies_confirmation_keyboard()
        )
        return CONFIRMING_STRATEGIES
    
    async def confirm_strategies_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle strategy confirmation"""
        query = update.callback_query
        await query.answer()
        
        action = query.data
        
        if action == "change_entry":
            # Go back to entry strategy selection
            await query.edit_message_text(
                "Select your entry strategy:",
                reply_markup=self.get_entry_strategy_keyboard()
            )
            return CHOOSING_ENTRY_STRATEGY
            
        elif action == "change_exit":
            # Go back to exit strategy selection
            await query.edit_message_text(
                "Select your exit strategy:",
                reply_markup=self.get_exit_strategy_keyboard()
            )
            return CHOOSING_EXIT_STRATEGY
            
        elif action == "confirm_strategies":
            # Check if we're in the initial subscription flow or post-subscription token selection
            user_id = query.from_user.id
            user = self.db.get_user_by_telegram_id(user_id)
            
            # Save the selected strategies to the database
            entry_strategy = context.user_data.get('entry_strategy', 'default')
            exit_strategy = context.user_data.get('exit_strategy', 'default')
            self.db.update_user_strategies(user_id, entry_strategy, exit_strategy)
            
            # Check if user is in initial subscription flow by looking for payment_data
            if 'payment_data' in context.user_data:
                # Continue to payment method selection (subscription flow)
                tier = context.user_data.get('selected_tier')
                selected_tokens = context.user_data.get('selected_tokens', [])
                entry_strategy_desc = context.user_data.get('entry_strategy_desc')
                exit_strategy_desc = context.user_data.get('exit_strategy_desc')
                
                # Create payment options
                payment_keyboard = [
                    [
                        InlineKeyboardButton("Pay with BTC", callback_data=f"pay_BTC_{tier}"),
                    ],
                    [
                        InlineKeyboardButton("Pay with SOL", callback_data=f"pay_SOL_{tier}"),
                    ],
                    [
                        InlineKeyboardButton("Pay with USDC", callback_data=f"pay_USDC_{tier}"),
                    ],
                    [
                        InlineKeyboardButton("Cancel", callback_data="cancel_payment")
                    ]
                ]
                
                # Prepare for payment
                await query.edit_message_text(
                    f"*Subscription Summary*\n\n"
                    f"*Tier:* {tier}\n"
                    f"*Selected Tokens:* {', '.join(selected_tokens)}\n"
                    f"*Entry Strategy:* {entry_strategy_desc}\n"
                    f"*Exit Strategy:* {exit_strategy_desc}\n\n"
                    f"Total: *${self.pricing[tier]}/month*\n\n"
                    "Please choose your payment method:",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup(payment_keyboard)
                )
                return CHOOSING_PAYMENT
            else:
                # Post-subscription flow - prompt for API key setup
                # Get display names for strategies
                entry_strategy_desc = context.user_data.get('entry_strategy_desc', 'Default')
                exit_strategy_desc = context.user_data.get('exit_strategy_desc', 'Default')
                
                # Offer options for next steps
                keyboard = [
                    [InlineKeyboardButton("Set up API Keys", callback_data="guide_keys")],
                    [InlineKeyboardButton("Start Bot", callback_data="confirm_start")]
                ]
                
                # Check if API keys are already set up
                kraken_key = self.db.get_api_key(user_id, 'kraken')
                hl_key = self.db.get_api_key(user_id, 'hyperliquid')
                
                if not kraken_key or not hl_key:
                    # User needs to set up API keys
                    await query.edit_message_text(
                        f"✅ Strategies saved successfully!\n\n"
                        f"*Entry Strategy:* {entry_strategy_desc}\n"
                        f"*Exit Strategy:* {exit_strategy_desc}\n\n"
                        f"Next step: Let's set up your API keys so you can start trading.",
                        parse_mode="Markdown",
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("Set up API Keys", callback_data="guide_keys")]
                        ])
                    )
                else:
                    # API keys are already set up, offer to start the bot
                    await query.edit_message_text(
                        f"✅ Strategies saved successfully!\n\n"
                        f"*Entry Strategy:* {entry_strategy_desc}\n"
                        f"*Exit Strategy:* {exit_strategy_desc}\n\n"
                        f"Your bot is configured and ready. You can now start trading!",
                        parse_mode="Markdown",
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("Start Bot", callback_data="confirm_start")]
                        ])
                    )
                
                return ConversationHandler.END
        
    async def payment_method_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handles payment method selection"""
        query = update.callback_query
        user_id = query.from_user.id
        
        await query.answer()
        
        # Get payment data from context
        payment_data = context.user_data.get('payment_data', {})
        tier = payment_data.get('tier', 1)
        amount = payment_data.get('amount', 50)
        email = payment_data.get('email', '')
        
        if not email:
            # If email is missing, get it from the database
            user = self.db.get_user_by_telegram_id(user_id)
            email = user.email if user and user.email else ''
        
        if query.data == "pay_boomfi":
            payment_manager = PaymentManager()
            
            # Generate payment request
            payment_request = payment_manager.generate_payment_request(
                user_id=user_id,
                amount=amount,
                tier=tier
            )
            
            if payment_request.get('success'):
                payment_id = payment_request.get('payment_id')
                checkout_url = payment_request.get('checkout_url')
                
                # Store transaction in database
                self.db.create_transaction(
                    user_id=user_id,
                    amount=amount,
                    tier=tier,
                    transaction_id=payment_id,
                    payment_data=json.dumps(payment_request)
                )
                
                # Send payment instructions
                email_reminder = f"**IMPORTANT**: Please use the email address '{email}' during checkout so we can correctly match your payment."
                
                await query.edit_message_text(
                    f"Please complete your payment for Tier {tier} (${amount}):\n\n"
                    f"{email_reminder}\n\n"
                    f"1. Click this link to pay: [Complete Payment]({checkout_url})\n"
                    f"2. Follow the instructions on the payment page.\n"
                    f"3. Your subscription will be activated once payment is confirmed.\n\n"
                    f"Payment ID: `{payment_id}`\n\n"
                    f"⏳ *We'll notify you here once your payment is confirmed.*",
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=True
                )
                
                # Don't start background task to check payment status immediately
                # We'll rely on the webhook for payment confirmation
            else:
                error = payment_request.get('error', 'Unknown error')
                await query.edit_message_text(
                    f"Sorry, there was an error generating your payment request: {error}\n\n"
                    f"Please try again later or contact support."
                )
        else:
            await query.edit_message_text(
                "Invalid payment method selected. Please try again."
            )
        
        return ConversationHandler.END
        
    async def handle_payment_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle callback after user returns from BoomFi payment page"""
        # This is called when user returns from payment page with /start payment_confirmed_XXXXX
        # Extract payment ID from the command
        message = update.message.text
        parts = message.split("_", 2)
        
        if len(parts) < 3:
            await update.message.reply_text(
                "Invalid payment callback. Please use /start to begin."
            )
            return ConversationHandler.END
            
        payment_id = parts[2]
        self.logger.info(f"Payment callback received for payment {payment_id}")
        
        # Check payment status in database
        transaction_data = self.db.get_transaction_with_user(payment_id)
        
        if not transaction_data:
            await update.message.reply_text(
                "Payment not found. Please use /subscribe to start a new subscription."
            )
            return ConversationHandler.END
            
        user_id = transaction_data['user_id']
        status = transaction_data['status']
        tier = transaction_data['tier']
        
        # Save the user's strategy selections if they exist
        if context.user_data.get('entry_strategy') and context.user_data.get('exit_strategy'):
            entry_strategy = context.user_data.get('entry_strategy')
            exit_strategy = context.user_data.get('exit_strategy')
            
            # Update user's strategy preferences in the database
            self.db.update_user_strategies(user_id, entry_strategy, exit_strategy)
            self.logger.info(f"Updated strategies for user {user_id}: entry={entry_strategy}, exit={exit_strategy}")
        
        if status == 'completed':
            # Payment is already verified
            await update.message.reply_text(
                f"✅ Your payment has been confirmed and your Tier {tier} subscription is active.\n\n"
                f"Let's set up your API keys so you can start trading.\n\n"
                f"Please enter your Kraken API Key:"
            )
            return AWAITING_KRAKEN_KEY
        else:
            # Payment is still pending - webhook may not have been received yet
            # Start the verification task to check
            asyncio.create_task(self.verify_payment_task(user_id, payment_id))
            
            # Tell the user we're verifying
            await update.message.reply_text(
                "🔄 We're verifying your cryptocurrency payment. This may take a few moments...\n\n"
                "You will receive a notification once your payment is confirmed."
            )
            
            return ConversationHandler.END
        
    async def cmd_tokens(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /tokens command to manage token selections"""
        user_id = update.effective_user.id
        user = self.db.get_user_by_telegram_id(user_id)
        
        if not user:
            # Handle direct command
            if hasattr(update, 'message') and update.message:
                await update.message.reply_text(
                    "Please use /start to register first."
                )
            # Handle callback from inline button
            elif hasattr(update, 'callback_query') and update.callback_query:
                await update.callback_query.message.reply_text(
                    "Please use /start to register first."
                )
            return ConversationHandler.END
            
        # Check if user has an active subscription
        if not user.subscription_tier or not user.subscription_expiry or user.subscription_expiry < datetime.now():
            # Handle direct command
            if hasattr(update, 'message') and update.message:
                await update.message.reply_text(
                    "You don't have an active subscription. Please subscribe first with /subscribe"
                )
            # Handle callback from inline button
            elif hasattr(update, 'callback_query') and update.callback_query:
                await update.callback_query.message.reply_text(
                    "You don't have an active subscription. Please subscribe first with /subscribe"
                )
            return ConversationHandler.END
            
        # Get current token selections
        current_tokens = self.db.get_user_tokens(user_id)
        max_tokens = self.token_limits[user.subscription_tier]
        
        # Refresh available pairs
        self.available_pairs = get_active_trading_pairs()
        
        # Create token selection UI
        token_buttons = []
        for token in self.available_pairs:
            if token in current_tokens:
                token_buttons.append([
                    InlineKeyboardButton(f"✅ {token}", callback_data=f"toggle_{token}")
                ])
            else:
                token_buttons.append([
                    InlineKeyboardButton(token, callback_data=f"toggle_{token}")
                ])
        
        token_buttons.append([
            InlineKeyboardButton("Save Selections", callback_data="save_tokens")
        ])
        
        # Store current tokens in context
        context.user_data['current_tokens'] = current_tokens.copy()
        
        # Format current selections text
        current_text = ", ".join(current_tokens) if current_tokens else "None"
        
        message_text = (
            f"*Token Selection*\n\n"
            f"Your subscription (Tier {user.subscription_tier}) allows you to select "
            f"up to {max_tokens} tokens.\n\n"
            f"*Current selections:* {current_text}\n"
            f"({len(current_tokens)}/{max_tokens})\n\n"
            f"Tap on tokens to select or deselect them. There are {len(self.available_pairs)} tokens available:"
        )
        
        # Handle direct command
        if hasattr(update, 'message') and update.message:
            await update.message.reply_text(
                message_text,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(token_buttons)
            )
        # Handle callback from inline button
        elif hasattr(update, 'callback_query') and update.callback_query:
            await update.callback_query.message.reply_text(
                message_text,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(token_buttons)
            )
        
        # Make sure we're clearing any existing conversations
        return CHOOSING_TOKENS
        
    async def manage_tokens_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle token management callbacks"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.db.get_user_by_telegram_id(user_id)
        
        if not user:
            await query.edit_message_text("User not found. Please use /start to register.")
            return ConversationHandler.END
            
        max_tokens = self.token_limits[user.subscription_tier]
        
        if query.data == "save_tokens":
            # Save the current token selections
            if 'current_tokens' in context.user_data:
                tokens = context.user_data['current_tokens']
                success = self.db.update_user_tokens(user_id, tokens)
                
                if success:
                    # Store selected tokens for use in the strategy selection
                    context.user_data['selected_tokens'] = tokens.copy()
                    
                    # Transition to entry strategy selection instead of ending conversation
                    await query.edit_message_text(
                        f"✅ Your token selections have been saved: *{', '.join(tokens) if tokens else 'None'}*\n\n"
                        f"Now, let's configure your *trading strategies*.\n\n"
                        f"Choose your *entry strategy*:",
                        parse_mode='Markdown',
                        reply_markup=self.get_entry_strategy_keyboard()
                    )
                    
                    return CHOOSING_ENTRY_STRATEGY
                else:
                    await query.edit_message_text(
                        "❌ There was a problem saving your token selections. Please try again."
                    )
                    
                    # Clear token selection state
                    if 'current_tokens' in context.user_data:
                        del context.user_data['current_tokens']
                    if 'in_token_selection' in context.user_data:  
                        del context.user_data['in_token_selection']
                        
                    return ConversationHandler.END
            else:
                await query.edit_message_text(
                    "⚠️ No token selections found. Please try again."
                )
                return ConversationHandler.END
            
        elif query.data.startswith("toggle_"):
            # Toggle a token selection
            token = query.data.split("_")[1]
            
            if 'current_tokens' not in context.user_data:
                context.user_data['current_tokens'] = []
                
            current_tokens = context.user_data['current_tokens']
            
            # Toggle the token
            if token in current_tokens:
                current_tokens.remove(token)
            else:
                # Check if max tokens reached
                if len(current_tokens) >= max_tokens:
                    await query.answer(f"Maximum {max_tokens} tokens for Tier {user.subscription_tier}. Deselect a token first.")
                    return CHOOSING_TOKENS
                    
                current_tokens.append(token)
                
            # Update UI
            token_buttons = []
            for available_token in self.available_pairs:
                if available_token in current_tokens:
                    token_buttons.append([
                        InlineKeyboardButton(f"✅ {available_token}", callback_data=f"toggle_{available_token}")
                    ])
                else:
                    token_buttons.append([
                        InlineKeyboardButton(available_token, callback_data=f"toggle_{available_token}")
                    ])
                    
            token_buttons.append([
                InlineKeyboardButton("Save Selections", callback_data="save_tokens")
            ])
            
            # Format current selections text
            current_text = ", ".join(current_tokens) if current_tokens else "None"
            
            try:
                await query.edit_message_text(
                    f"*Token Selection*\n\n"
                    f"Your subscription (Tier {user.subscription_tier}) allows you to select "
                    f"up to {max_tokens} tokens.\n\n"
                    f"*Current selections:* {current_text}\n"
                    f"({len(current_tokens)}/{max_tokens})\n\n"
                    f"Tap on tokens to select or deselect them. There are {len(self.available_pairs)} tokens available:",
                    parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup(token_buttons)
                )
            except Exception as e:
                logger.error(f"Error updating token selection message: {str(e)}")
                # If we can't edit the message, send a new one
                await query.message.reply_text(
                    f"*Token Selection*\n\n"
                    f"Your subscription (Tier {user.subscription_tier}) allows you to select "
                    f"up to {max_tokens} tokens.\n\n"
                    f"*Current selections:* {current_text}\n"
                    f"({len(current_tokens)}/{max_tokens})\n\n"
                    f"Tap on tokens to select or deselect them. There are {len(self.available_pairs)} tokens available:",
                    parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup(token_buttons)
                )
                
            return CHOOSING_TOKENS
            
        return CHOOSING_TOKENS
        
    async def cmd_setkeys(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /setkeys command"""
        user_id = update.effective_user.id
        user = self.db.get_user_by_telegram_id(user_id)
        
        if not user:
            # Handle direct command
            if hasattr(update, 'message') and update.message:
                await update.message.reply_text(
                    "Please use /start to register first."
                )
            # Handle callback from inline button
            elif hasattr(update, 'callback_query') and update.callback_query:
                await update.callback_query.message.reply_text(
                    "Please use /start to register first."
                )
            return ConversationHandler.END
            
        # Check if user has an active subscription
        if not user.subscription_tier or not user.subscription_expiry or user.subscription_expiry < datetime.now():
            # Handle direct command
            if hasattr(update, 'message') and update.message:
                await update.message.reply_text(
                    "You don't have an active subscription. Please subscribe first with /subscribe"
                )
            # Handle callback from inline button
            elif hasattr(update, 'callback_query') and update.callback_query:
                await update.callback_query.message.reply_text(
                    "You don't have an active subscription. Please subscribe first with /subscribe"
                )
            return ConversationHandler.END
            
        message_text = (
            "🔑 Let's set up your API keys.\n\n"
            "⚠️ *IMPORTANT*: Never share your API keys with anyone else!\n\n"
            "First, please enter your Kraken API Key:"
        )
        
        # Handle direct command
        if hasattr(update, 'message') and update.message:
            await update.message.reply_text(
                message_text,
                parse_mode='Markdown'
            )
        # Handle callback from inline button
        elif hasattr(update, 'callback_query') and update.callback_query:
            await update.callback_query.message.reply_text(
                message_text,
                parse_mode='Markdown'
            )
        
        # Make sure we're clearing any existing conversations and starting fresh
        return AWAITING_KRAKEN_KEY
        
    async def process_kraken_key(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process Kraken API key input"""
        try:
            logger.info(f"Processing Kraken API key from user {update.effective_user.id}")
            
            # Delete the message containing the API key for security
            await update.message.delete()
            
            # Store the API key securely
            context.user_data['kraken_key'] = update.message.text
            
            # Send a confirmation message
            msg = await update.message.reply_text(
                "✅ Kraken API Key received.\n\n"
                "Now, please enter your Kraken API Secret:"
            )
            
            logger.info(f"Transitioning to AWAITING_KRAKEN_SECRET state for user {update.effective_user.id}")
            return AWAITING_KRAKEN_SECRET
        except Exception as e:
            logger.error(f"Error processing Kraken API key: {str(e)}")
            await update.message.reply_text(
                "❌ There was an error processing your API key. Please try again with /setkeys"
            )
            return ConversationHandler.END
        
    async def process_kraken_secret(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process Kraken API secret input"""
        try:
            logger.info(f"Processing Kraken API secret from user {update.effective_user.id}")
            
            # Delete the message containing the API secret for security
            await update.message.delete()
            
            # Store the API secret securely
            context.user_data['kraken_secret'] = update.message.text
            
            # Send a confirmation message
            msg = await update.message.reply_text(
                "✅ Kraken API Secret received.\n\n"
                "Now, please enter your Hyperliquid API Key:"
            )
            
            logger.info(f"Transitioning to AWAITING_HL_KEY state for user {update.effective_user.id}")
            return AWAITING_HL_KEY
        except Exception as e:
            logger.error(f"Error processing Kraken API secret: {str(e)}")
            await update.message.reply_text(
                "❌ There was an error processing your API secret. Please try again with /setkeys"
            )
            return ConversationHandler.END
        
    async def process_hl_key(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process Hyperliquid API key input"""
        try:
            logger.info(f"Processing Hyperliquid API key from user {update.effective_user.id}")
            
            # Delete the message containing the API key for security
            await update.message.delete()
            
            # Store the API key securely
            context.user_data['hl_key'] = update.message.text
            
            # Send a confirmation message
            msg = await update.message.reply_text(
                "✅ Hyperliquid API Key received.\n\n"
                "Finally, please enter your Hyperliquid API Secret:"
            )
            
            logger.info(f"Transitioning to AWAITING_HL_SECRET state for user {update.effective_user.id}")
            return AWAITING_HL_SECRET
        except Exception as e:
            logger.error(f"Error processing Hyperliquid API key: {str(e)}")
            await update.message.reply_text(
                "❌ There was an error processing your API key. Please try again with /setkeys"
            )
            return ConversationHandler.END
        
    async def process_hl_secret(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process Hyperliquid API secret input"""
        try:
            logger.info(f"Processing Hyperliquid API secret from user {update.effective_user.id}")
            
            # Delete the message containing the API secret for security
            await update.message.delete()
            
            # Store the API secret temporarily
            context.user_data['hl_secret'] = update.message.text
            
            # Ask for Hyperliquid wallet address
            await update.message.reply_text(
                "Now, please provide your Hyperliquid wallet address (starting with 0x).\n\n"
                "This is needed to check your account balance and enable percentage-based position sizing.",
                reply_markup=ReplyKeyboardRemove()
            )
            
            logger.info(f"Transitioning to AWAITING_HL_ADDRESS state for user {update.effective_user.id}")
            return AWAITING_HL_ADDRESS
            
        except Exception as e:
            logger.error(f"Error in process_hl_secret for user {update.effective_user.id}: {str(e)}")
            await update.message.reply_text(
                "❌ There was an error processing your API keys. Please try again with /setkeys"
            )
            return ConversationHandler.END
        
    async def process_hl_address(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process Hyperliquid address input"""
        try:
            logger.info(f"Processing Hyperliquid address from user {update.effective_user.id}")
            user_id = update.effective_user.id
            
            # Validate the address format
            address = update.message.text.strip().lower()
            if not address.startswith('0x') or len(address) != 42:
                await update.message.reply_text(
                    "⚠️ Invalid Ethereum address format. Please provide a valid Hyperliquid wallet address starting with 0x.",
                    reply_markup=ReplyKeyboardRemove()
                )
                return AWAITING_HL_ADDRESS
                
            # Store the address temporarily
            context.user_data['hl_address'] = address
            
            # Get all API keys from user data
            kraken_key = context.user_data.get('kraken_key')
            kraken_secret = context.user_data.get('kraken_secret')
            hl_key = context.user_data.get('hl_key')
            hl_secret = context.user_data.get('hl_secret')
            hl_address = context.user_data.get('hl_address')
            
            logger.info(f"All API keys and address collected for user {user_id}, proceeding to store them securely")
            
            # Encrypt and store Kraken API keys
            kraken_key_success = False
            hl_key_success = False
            
            if kraken_key and kraken_secret:
                try:
                    logger.info(f"Encrypting Kraken API keys for user {user_id}")
                    encrypted_kraken_key, iv_kraken_key = self.security.encrypt(kraken_key)
                    encrypted_kraken_secret, iv_kraken_secret = self.security.encrypt(kraken_secret)
                    
                    kraken_key_success = self.db.store_api_key(
                        telegram_id=user_id,
                        exchange='kraken',
                        encrypted_key=encrypted_kraken_key,
                        encrypted_secret=encrypted_kraken_secret,
                        key_iv=iv_kraken_key,
                        secret_iv=iv_kraken_secret
                    )
                    logger.info(f"Kraken API keys storage {'successful' if kraken_key_success else 'failed'} for user {user_id}")
                except Exception as e:
                    logger.error(f"Error encrypting Kraken API keys for user {user_id}: {str(e)}")
                    
            # Encrypt and store Hyperliquid API keys
            if hl_key and hl_secret:
                try:
                    logger.info(f"Encrypting Hyperliquid API keys for user {user_id}")
                    encrypted_hl_key, iv_hl_key = self.security.encrypt(hl_key)
                    encrypted_hl_secret, iv_hl_secret = self.security.encrypt(hl_secret)
                    
                    hl_key_success = self.db.store_api_key(
                        telegram_id=user_id,
                        exchange='hyperliquid',
                        encrypted_key=encrypted_hl_key,
                        encrypted_secret=encrypted_hl_secret,
                        key_iv=iv_hl_key,
                        secret_iv=iv_hl_secret
                    )
                    logger.info(f"Hyperliquid API keys storage {'successful' if hl_key_success else 'failed'} for user {user_id}")
                except Exception as e:
                    logger.error(f"Error encrypting Hyperliquid API keys for user {user_id}: {str(e)}")
                    
            # Store Hyperliquid address
            address_success = False
            if hl_address:
                try:
                    logger.info(f"Storing Hyperliquid address for user {user_id}")
                    address_success = self.db.update_user_hl_address(user_id, hl_address)
                    logger.info(f"Hyperliquid address storage {'successful' if address_success else 'failed'} for user {user_id}")
                except Exception as e:
                    logger.error(f"Error storing Hyperliquid address for user {user_id}: {str(e)}")
                    
            # Clear API keys from context for security
            logger.info(f"Clearing sensitive data from context for user {user_id}")
            if 'kraken_key' in context.user_data:
                del context.user_data['kraken_key']
            if 'kraken_secret' in context.user_data:
                del context.user_data['kraken_secret']
            if 'hl_key' in context.user_data:
                del context.user_data['hl_key']
            if 'hl_secret' in context.user_data:
                del context.user_data['hl_secret']
            if 'hl_address' in context.user_data:
                del context.user_data['hl_address']
            if 'setting_api_keys' in context.user_data:  
                del context.user_data['setting_api_keys']
                
            # Show confirmation message
            if kraken_key_success and hl_key_success and address_success:
                logger.info(f"All API keys and address successfully stored for user {user_id}")
                msg = await update.message.reply_text(
                    "🔐 All API keys and wallet address have been securely stored.\n\n"
                    "You can now use /tokens to select which tokens to trade,\n"
                    "and /start_bot to begin trading."
                )
            elif not address_success:
                logger.warning(f"Failed to store Hyperliquid address for user {user_id}")
                msg = await update.message.reply_text(
                    "🔐 API keys have been securely stored, but there was an issue with your Hyperliquid address.\n\n"
                    "Please try setting your keys again with /setkeys."
                )
            elif kraken_key_success and not hl_key_success:
                logger.warning(f"Only Kraken API keys were stored successfully for user {user_id}")
                msg = await update.message.reply_text(
                    "🔐 Kraken API keys and Hyperliquid address have been securely stored.\n\n"
                    "However, there was an issue with your Hyperliquid API keys. "
                    "Please try setting them again with /setkeys."
                )
            elif hl_key_success and not kraken_key_success:
                logger.warning(f"Only Hyperliquid API keys were stored successfully for user {user_id}")
                msg = await update.message.reply_text(
                    "🔐 Hyperliquid API keys and address have been securely stored.\n\n"
                    "However, there was an issue with your Kraken API keys. "
                    "Please try setting them again with /setkeys."
                )
            else:
                logger.error(f"Failed to store any API keys for user {user_id}")
                msg = await update.message.reply_text(
                    "❌ There was an issue storing your API keys. Please try again with /setkeys."
                )
                
            logger.info(f"API key setup completed for user {user_id}")
            return ConversationHandler.END
            
        except Exception as e:
            logger.error(f"Error in process_hl_address for user {update.effective_user.id}: {str(e)}")
            await update.message.reply_text(
                "❌ There was an error processing your Hyperliquid address. Please try again with /setkeys"
            )
            return ConversationHandler.END
    
    async def cmd_start_bot(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start_bot command"""
        user_id = update.effective_user.id
        user = self.db.get_user_by_telegram_id(user_id)
        
        if not user:
            await update.message.reply_text(
                "Please use /start to register first."
            )
            return ConversationHandler.END
            
        # Check for active subscription
        if not user.subscription_tier or not user.subscription_expiry or user.subscription_expiry < datetime.now():
            await update.message.reply_text(
                "You don't have an active subscription. Please subscribe first with /subscribe"
            )
            return ConversationHandler.END
            
        # Check if API keys are set
        kraken_key = self.db.get_api_key(user_id, 'kraken')
        hl_key = self.db.get_api_key(user_id, 'hyperliquid')
        
        if not kraken_key or not hl_key:
            await update.message.reply_text(
                "You need to set up your API keys first with /setkeys"
            )
            return ConversationHandler.END
            
        # Check if bot is already running
        bot_status = self.db.get_bot_status(user_id)
        if bot_status and bot_status.is_running:
            await update.message.reply_text(
                "Your bot is already running. You can check its status with /status"
            )
            return ConversationHandler.END
            
        # Get selected tokens
        selected_tokens = self.db.get_user_tokens(user_id)
        
        if not selected_tokens:
            await update.message.reply_text(
                "You haven't selected any tokens to trade. Please use /tokens to select trading pairs."
            )
            return ConversationHandler.END
            
        # Show confirmation
        keyboard = [
            [
                InlineKeyboardButton("✅ Start Bot", callback_data="confirm_start"),
                InlineKeyboardButton("❌ Cancel", callback_data="cancel_start")
            ]
        ]
        
        tokens_text = ", ".join(selected_tokens)
            
        await update.message.reply_text(
            f"You're about to start the Abraxas Greenprint Funding Bot (Tier {user.subscription_tier})\n\n"
            f"*Trading tokens:* {tokens_text}\n\n"
            "The bot will use your API keys to place trades on Hyperliquid and Kraken.\n\n"
            "Are you sure you want to start the bot?",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        return CONFIRM_START
        
    async def confirm_start_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle bot start confirmation"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "confirm_start":
            user_id = query.from_user.id
            user = self.db.get_user_by_telegram_id(user_id)
            
            # Decrypt API keys
            kraken_key = self.db.get_api_key(user_id, 'kraken')
            hl_key = self.db.get_api_key(user_id, 'hyperliquid')
            
            if not kraken_key or not hl_key:
                await query.edit_message_text(
                    "❌ Failed to start bot: API keys not found. Please set them with /setkeys"
                )
                return ConversationHandler.END
                
            # Get Hyperliquid address
            hl_address = self.db.get_user_hl_address(user_id)
            if not hl_address:
                await query.edit_message_text(
                    "❌ Hyperliquid wallet address not found. Please set up your API keys again with /setkeys"
                )
                return ConversationHandler.END
                
            # Get selected tokens
            selected_tokens = self.db.get_user_tokens(user_id)
            
            if not selected_tokens:
                await query.edit_message_text(
                    "❌ No tokens selected for trading. Please use /tokens to select tokens first."
                )
                return ConversationHandler.END
                
            # Decrypt the keys
            kraken_api_key = self.security.decrypt(kraken_key.encrypted_key, kraken_key.key_iv)
            kraken_api_secret = self.security.decrypt(kraken_key.encrypted_secret, kraken_key.secret_iv)
            hl_api_key = self.security.decrypt(hl_key.encrypted_key, hl_key.key_iv)
            hl_api_secret = self.security.decrypt(hl_key.encrypted_secret, hl_key.secret_iv)
            
            try:
                # Show loading message
                await query.edit_message_text(
                    "🔄 Starting bot and checking balances on Kraken and Hyperliquid...\n\n"
                    "This may take a moment."
                )
                
                # Start the trading bot with selected tokens
                success = self.bot_service.start_bot(
                    user_id=str(user_id),
                    tier=user.subscription_tier,
                    kraken_key=kraken_api_key,
                    kraken_secret=kraken_api_secret,
                    hl_key=hl_api_key,
                    hl_secret=hl_api_secret,
                    hl_address=hl_address,
                    selected_tokens=selected_tokens
                )
                
                if success:
                    # Update bot status in database
                    self.db.update_bot_status(
                        telegram_id=user_id,
                        is_running=True,
                        start_time=datetime.now()
                    )
                    
                    # Format tokens for display
                    tokens_text = ", ".join(selected_tokens)
                    
                    await query.edit_message_text(
                        "🚀 Abraxas Greenprint Funding Bot started successfully!\n\n"
                        f"*Trading tokens:* {tokens_text}\n\n"
                        "Your bot is now running and will automatically trade based on funding rates.\n\n"
                        "You can check its status anytime with /status\n"
                        "To stop the bot, use /stop_bot",
                        parse_mode='Markdown'
                    )
                else:
                    await query.edit_message_text(
                        "❌ Failed to start the bot.\n\n"
                        "Common issues:\n"
                        "• Insufficient balance on Kraken or Hyperliquid\n"
                        "• Invalid API keys or wallet address\n"
                        "• Exchange connection issues\n\n"
                        "Please check your balances and try again."
                    )
            except Exception as e:
                logger.error(f"Error starting bot for user {user_id}: {str(e)}")
                # Remove Markdown for error messages to avoid parsing issues
                await query.edit_message_text(
                    f"❌ An error occurred while starting the bot: {str(e)}",
                    parse_mode=None  # Disable Markdown for error messages
                )
                
        elif query.data == "cancel_start":
            await query.edit_message_text("Bot start cancelled.")
            
        return ConversationHandler.END
        
    async def cmd_stop_bot(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /stop_bot command"""
        user_id = update.effective_user.id
        
        # Check if bot is running
        bot_status = self.db.get_bot_status(user_id)
        if not bot_status or not bot_status.is_running:
            await update.message.reply_text(
                "Your bot is not currently running. You can start it with /start_bot"
            )
            return ConversationHandler.END
            
        # Show confirmation
        keyboard = [
            [
                InlineKeyboardButton("⚠️ Stop Bot", callback_data="confirm_stop"),
                InlineKeyboardButton("Cancel", callback_data="cancel_stop")
            ]
        ]
        
        await update.message.reply_text(
            "⚠️ Are you sure you want to stop your trading bot?\n\n"
            "This will close all open orders and exit active positions.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        return CONFIRM_STOP
        
    async def confirm_stop_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle bot stop confirmation"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "confirm_stop":
            user_id = query.from_user.id
            
            try:
                # Stop the trading bot
                success = self.bot_service.stop_bot(str(user_id))
                
                if success:
                    # Update bot status in database
                    self.db.update_bot_status(
                        telegram_id=user_id,
                        is_running=False,
                        stop_time=datetime.now()
                    )
                    
                    await query.edit_message_text(
                        "✅ Bot stopped successfully.\n\n"
                        "All positions have been closed and trading has stopped."
                    )
                else:
                    await query.edit_message_text(
                        "❌ Failed to stop the bot. Please try again or contact support."
                    )
            except Exception as e:
                logger.error(f"Error stopping bot for user {user_id}: {str(e)}")
                await query.edit_message_text(
                    f"❌ An error occurred while stopping the bot: {str(e)}"
                )
                
        elif query.data == "cancel_stop":
            await query.edit_message_text("Bot will continue running.")
            
        return ConversationHandler.END
        
    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /status command"""
        user_id = update.effective_user.id
        user = self.db.get_user_by_telegram_id(user_id)
        
        if not user:
            await update.message.reply_text(
                "Please use /start to register first."
            )
            return
            
        # Get subscription info
        subscription_status = "No active subscription"
        if user.subscription_tier and user.subscription_expiry:
            if user.subscription_expiry > datetime.now():
                days_left = (user.subscription_expiry - datetime.now()).days
                subscription_status = f"Tier {user.subscription_tier} - {days_left} days left"
            else:
                subscription_status = f"Tier {user.subscription_tier} - Expired"
                
        # Get selected tokens
        selected_tokens = self.db.get_user_tokens(user_id)
        token_status = ", ".join(selected_tokens) if selected_tokens else "None"
                
        # Get bot status
        bot_status = self.db.get_bot_status(user_id)
        status_text = "Not running"
        uptime = "N/A"
        
        if bot_status and bot_status.is_running:
            status_text = "🟢 Running"
            if bot_status.start_time:
                uptime_seconds = (datetime.now() - bot_status.start_time).total_seconds()
                hours, remainder = divmod(uptime_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                uptime = f"{int(hours)}h {int(minutes)}m"
                
        # Get actual bot positions from service if running
        positions_text = "No active positions"
        if bot_status and bot_status.is_running:
            bot_info = self.bot_service.get_bot_status(str(user_id))
            if bot_info and 'positions' in bot_info and bot_info['positions']:
                positions_text = ""
                for asset, pos in bot_info['positions'].items():
                    positions_text += f"\n{asset}: HL={pos['hl_position']}, Kraken={pos['kraken_position']}"
                    
        # Format status message
        status_message = (
            "📊 *Abraxas Greenprint Status*\n\n"
            f"*Subscription:* {subscription_status}\n"
            f"*Selected Tokens:* {token_status}\n"
            f"*Bot Status:* {status_text}\n"
            f"*Uptime:* {uptime}\n\n"
            f"*Active Positions:*\n{positions_text}\n\n"
            f"Commands:\n"
            f"• /tokens - Change your token selections\n"
            f"• /start_bot - Start trading\n"
            f"• /stop_bot - Stop trading"
        )
        
        await update.message.reply_text(status_message, parse_mode='Markdown')
        
    async def cancel_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancel current conversation"""
        await update.message.reply_text(
            "Operation cancelled."
        )
        return ConversationHandler.END
        
    async def unknown_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle unknown commands"""
        command = update.message.text.split()[0]  # Get the command part
        
        # List all recognized commands
        valid_commands = ["/start", "/help", "/pairs", "/subscribe", "/tokens", 
                         "/setkeys", "/status", "/start_bot", "/stop_bot", "/cancel"]
        
        self.logger.info(f"Received command: {command}")
        
        if command in valid_commands:
            # It's a valid command but wasn't properly handled
            self.logger.error(f"Command {command} not properly processed despite being valid")
            await update.message.reply_text(
                f"Command {command} was recognized but could not be processed. "
                "Please try again or use /start to restart the bot."
            )
        else:
            # Truly unknown command
            self.logger.warning(f"Unknown command received: {command}")
            await update.message.reply_text(
                f"Sorry, I don't understand the command '{command}'. "
                "Use /help to see available commands."
            )
        
    async def verify_payment_task(self, user_id, payment_id):
        """Background task to verify payment"""
        try:
            self.logger.info(f"Starting payment verification for user {user_id}, payment {payment_id}")
            
            # Get transaction data
            transaction_data = self.db.get_transaction(payment_id)
            if not transaction_data:
                self.logger.error(f"Transaction {payment_id} not found in database")
                return
            
            # Check if payment is already confirmed
            if transaction_data['status'] == 'completed':
                self.logger.info(f"Payment {payment_id} already confirmed")
                return
            
            # Get payment data
            payment_data = json.loads(transaction_data['payment_data'])
            tier = transaction_data['tier']
            
            # First, quickly check if webhook has already confirmed the payment
            transaction_data = self.db.get_transaction(payment_id)
            if transaction_data['status'] == 'completed':
                # Payment already confirmed via webhook!
                self.logger.info(f"Payment {payment_id} already confirmed via webhook")
                await self._send_confirmation_and_setup_keys(user_id, payment_id, tier)
                return
                
            # Wait for payment confirmation via webhook with patience
            # More attempts with longer increasing intervals
            wait_times = [10, 15, 20, 30, 45]  # seconds
            
            for attempt, wait_time in enumerate(wait_times):
                self.logger.info(f"Verifying payment attempt {attempt+1}/{len(wait_times)}")
                
                # Check payment status in our database (may have been updated by webhook)
                transaction_data = self.db.get_transaction(payment_id)
                
                if transaction_data['status'] == 'completed':
                    # Payment confirmed via webhook!
                    self.logger.info(f"Payment {payment_id} confirmed via webhook on attempt {attempt+1}")
                    await self._send_confirmation_and_setup_keys(user_id, payment_id, tier)
                    return
                
                # Try direct API verification every other attempt
                if attempt % 2 == 1:
                    if self.payment.verify_payment(payment_id):
                        self.logger.info(f"Payment {payment_id} confirmed via API on attempt {attempt+1}")
                        
                        # Update transaction status
                        self.db.update_transaction_status(payment_id, 'completed')
                        
                        await self._send_confirmation_and_setup_keys(user_id, payment_id, tier)
                        return
                
                # Tell the user we're still working on it if it's taking a while
                if attempt == 2:  # Send after ~45 seconds
                    await self.application.bot.send_message(
                        chat_id=user_id,
                        text="We're still verifying your payment... This may take a moment. We'll notify you as soon as it's confirmed."
                    )
                
                # Wait before next attempt
                await asyncio.sleep(wait_time)
            
            # If we get here, try one final direct verification
            if self.payment.verify_payment(payment_id):
                self.logger.info(f"Payment {payment_id} confirmed via API on final attempt")
                
                # Update transaction status
                self.db.update_transaction_status(payment_id, 'completed')
                
                await self._send_confirmation_and_setup_keys(user_id, payment_id, tier)
            else:
                # Payment not confirmed after all attempts
                self.logger.warning(f"Payment {payment_id} not confirmed after {len(wait_times)} verification attempts")
                
                # Send notification to user
                await self.application.bot.send_message(
                    chat_id=user_id,
                    text="⏳ We haven't been able to confirm your payment yet.\n\n"
                         "If you've completed the payment, this might take a few more minutes depending on blockchain confirmation times.\n\n"
                         "You'll receive a notification once it's confirmed, or you can check your status with /status."
                )
        
        except Exception as e:
            self.logger.error(f"Error in payment verification: {str(e)}")
            # Send error notification to user
            try:
                await self.application.bot.send_message(
                    chat_id=user_id,
                    text="❌ There was an error verifying your payment. Please contact support."
                )
            except:
                pass
                
    async def _send_confirmation_and_setup_keys(self, user_id, payment_id, tier):
        """Helper method to send payment confirmation and start API key setup"""
        try:
            # Update subscription
            from datetime import datetime, timedelta
            self.db.update_user_subscription(
                telegram_id=user_id,
                tier=tier,
                expiry=datetime.now() + timedelta(days=30)
            )
            
            # Send confirmation to user
            await self.application.bot.send_message(
                chat_id=user_id,
                text=f"✅ *Payment Confirmed Successfully!* Your Tier {tier} subscription is now active.\n\n"
                      f"🔐 *Next Step: Set up your API keys*\n\n"
                      f"To start trading, we need your exchange API keys. Please enter your Kraken API Key now:",
                parse_mode='Markdown'
            )
            
            # Start the API key setup conversation
            await self._start_key_setup_conversation(user_id)
            
        except Exception as e:
            self.logger.error(f"Error sending confirmation and setting up keys: {str(e)}")
            # Send a fallback message
            try:
                await self.application.bot.send_message(
                    chat_id=user_id,
                    text=f"✅ Your payment has been confirmed! Your Tier {tier} subscription is now active.\n\n"
                          "Please use /setkeys to set up your exchange API keys."
                )
            except:
                pass
        
    async def _start_key_setup_conversation(self, user_id):
        """Helper method to start the API key setup conversation"""
        try:
            # Create a new conversation context for this user
            chat_data = {}
            user_data = {}
            
            # Simulate the /setkeys command in a new conversation
            await self.cmd_setkeys(
                Update(
                    update_id=0,
                    message=Message(
                        message_id=0,
                        date=datetime.now(),
                        chat=Chat(id=user_id, type="private"),
                        from_user=User(id=user_id, is_bot=False, first_name="User"),
                        text="/setkeys"
                    )
                ),
                ContextTypes.DEFAULT_TYPE.from_dict({
                    'chat_data': chat_data,
                    'user_data': user_data
                })
            )
            
            self.logger.info(f"Started API key setup conversation for user {user_id}")
        except Exception as e:
            self.logger.error(f"Error starting key setup conversation: {str(e)}")
            # Fallback to manual command
            await self.application.bot.send_message(
                chat_id=user_id,
                text="To set up your API keys, please use the /setkeys command."
            )
        
    async def subscription_extend_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle subscription extension callback"""
        query = update.callback_query
        user_id = query.from_user.id
        
        await query.answer()
        
        # Check if this is a tier selection from extension flow
        if query.data.startswith("tier_"):
            # Process tier selection
            selected_tier = int(query.data.split("_")[1])
            
            # Store selected tier in context
            context.user_data['selected_tier'] = selected_tier
            
            # Initialize payment_data if not exists
            if 'payment_data' not in context.user_data:
                context.user_data['payment_data'] = {}
            
            context.user_data['payment_data']['tier'] = selected_tier
            
            # Get user's email from database
            user = self.db.get_user_by_telegram_id(user_id)
            existing_email = user.email if user and user.email else ""
            
            # Set up for payment by asking for email confirmation
            email_prompt = (
                f"You've selected Tier {selected_tier} for your subscription extension.\n\n"
            )
            
            if existing_email:
                email_prompt += (
                    f"We have your email on file as: {existing_email}\n\n"
                    f"Please confirm this email address is correct by typing it again, "
                    f"or enter a new email address:"
                )
            else:
                email_prompt += (
                    f"Before proceeding with payment, we need your email address to associate with your subscription.\n\n"
                    f"Please enter your email address:"
                )
            
            await query.edit_message_text(email_prompt)
            
            # This starts the email entry conversation
            return PAYMENT_EMAIL_ENTRY
            
        # Get the user's current subscription
        user = self.db.get_user_by_telegram_id(user_id)
        if not user or not user.subscription_tier:
            await query.edit_message_text(
                "Error: Subscription information not found. Please use /subscribe to start a new subscription."
            )
            return ConversationHandler.END
        
        current_tier = user.subscription_tier
        
        # Prepare tier options with correct pricing
        keyboard = []
        
        # Keep current tier option
        tier_prices = {1: 50, 2: 100, 3: 200}
        keyboard.append([InlineKeyboardButton(
            f"Keep Tier {current_tier} (${tier_prices[current_tier]}/month)", 
            callback_data=f"tier_{current_tier}"
        )])
        
        # Add upgrade/downgrade options
        if current_tier == 1:
            keyboard.append([InlineKeyboardButton("Upgrade to Tier 2 ($100/month)", callback_data="tier_2")])
            keyboard.append([InlineKeyboardButton("Upgrade to Tier 3 ($200/month)", callback_data="tier_3")])
        elif current_tier == 2:
            keyboard.append([InlineKeyboardButton("Downgrade to Tier 1 ($50/month)", callback_data="tier_1")])
            keyboard.append([InlineKeyboardButton("Upgrade to Tier 3 ($200/month)", callback_data="tier_3")])
        elif current_tier == 3:
            keyboard.append([InlineKeyboardButton("Downgrade to Tier 1 ($50/month)", callback_data="tier_1")])
            keyboard.append([InlineKeyboardButton("Downgrade to Tier 2 ($100/month)", callback_data="tier_2")])
        
        await query.edit_message_text(
            f"You currently have a Tier {current_tier} subscription.\n\n"
            f"Please select the tier you'd like to extend with:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        # Make sure we're using the subscription conversation
        logger.info(f"User {user_id} is selecting a tier for subscription extension")
        return CHOOSING_TIER
        
    async def cancel_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle cancel callback"""
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text(
            "Operation cancelled. Your subscription remains unchanged."
        )
        
    async def guide_tokens_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle guided token setup button from webhook notification"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        
        # End any existing conversations to avoid state conflicts
        context.user_data.clear()
        
        # Send a temporary confirmation message
        message = await query.edit_message_text("Taking you to token selection...")
        
        # Now create a new message with token selection options - this is better than
        # directly calling cmd_tokens which might have conversation state issues
        user = self.db.get_user_by_telegram_id(user_id)
        if not user:
            await message.reply_text("Please use /start to register first.")
            return ConversationHandler.END
            
        # Check if user has an active subscription
        if not user.subscription_tier or not user.subscription_expiry or user.subscription_expiry < datetime.now():
            await message.reply_text("You don't have an active subscription. Please subscribe first with /subscribe")
            return ConversationHandler.END
            
        # Get current token selections
        current_tokens = self.db.get_user_tokens(user_id)
        max_tokens = self.token_limits[user.subscription_tier]
        
        # Refresh available pairs
        self.available_pairs = get_active_trading_pairs()
        
        # Create token selection UI
        token_buttons = []
        for token in self.available_pairs:
            if token in current_tokens:
                token_buttons.append([
                    InlineKeyboardButton(f"✅ {token}", callback_data=f"toggle_{token}")
                ])
            else:
                token_buttons.append([
                    InlineKeyboardButton(token, callback_data=f"toggle_{token}")
                ])
        
        token_buttons.append([
            InlineKeyboardButton("Save Selections", callback_data="save_tokens")
        ])
        
        # Store current tokens in context
        context.user_data['current_tokens'] = current_tokens.copy()
        context.user_data['in_token_selection'] = True  # Flag to track state
        
        # Format current selections text
        current_text = ", ".join(current_tokens) if current_tokens else "None"
        
        message_text = (
            f"*Token Selection*\n\n"
            f"Your subscription (Tier {user.subscription_tier}) allows you to select "
            f"up to {max_tokens} tokens.\n\n"
            f"*Current selections:* {current_text}\n"
            f"({len(current_tokens)}/{max_tokens})\n\n"
            f"Tap on tokens to select or deselect them. There are {len(self.available_pairs)} tokens available:"
        )
        
        await message.reply_text(
            message_text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(token_buttons)
        )
        
        return CHOOSING_TOKENS
        
    async def guide_keys_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle guided API keys setup button from webhook notification"""
        try:
            query = update.callback_query
            await query.answer()
            
            user_id = update.effective_user.id
            logger.info(f"Guided API keys setup started for user {user_id}")
            
            # Clear user data to start fresh
            context.user_data.clear()
            context.user_data['setting_api_keys'] = True
            
            # Check if user has an active subscription
            user = self.db.get_user_by_telegram_id(user_id)
            if not user:
                logger.warning(f"User {user_id} not found in database")
                await query.edit_message_text("Please use /start to register first.")
                return ConversationHandler.END
                
            if not user.subscription_tier or not user.subscription_expiry or user.subscription_expiry < datetime.now():
                logger.warning(f"User {user_id} does not have an active subscription")
                await query.edit_message_text("You don't have an active subscription. Please subscribe first with /subscribe")
                return ConversationHandler.END
            
            # Start collecting API keys - directly edit the current message
            await query.edit_message_text(
                "🔑 Let's set up your API keys.\n\n"
                "⚠️ *IMPORTANT*: Never share your API keys with anyone else!\n\n"
                "First, please enter your Kraken API Key:",
                parse_mode='Markdown'
            )
            
            logger.info(f"Entering AWAITING_KRAKEN_KEY state for user {user_id}")
            return AWAITING_KRAKEN_KEY
        except Exception as e:
            logger.error(f"Error in guide_keys_callback: {str(e)}")
            await update.callback_query.edit_message_text(
                "❌ There was an error setting up API keys. Please try again with /setkeys"
            )
            return ConversationHandler.END
    
    async def guide_strategies_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Guide the user through selecting entry and exit strategies"""
        query = update.callback_query
        user_id = query.from_user.id
        
        try:
            logger.info(f"User {user_id} starting guided strategy setup")
            
            await query.answer()
            
            # Get the user from database
            user = self.db.get_user_by_telegram_id(user_id)
            if not user:
                logger.warning(f"User {user_id} not found in database for strategy setup")
                await query.edit_message_text(
                    "⚠️ User not found. Please use /start to register first."
                )
                return ConversationHandler.END
                
            # Check if user has an active subscription
            if not user.subscription_tier or not user.subscription_expiry or user.subscription_expiry < datetime.now():
                logger.warning(f"User {user_id} has no active subscription for strategy setup")
                await query.edit_message_text(
                    "⚠️ You don't have an active subscription. Please subscribe first with /subscribe"
                )
                return ConversationHandler.END
                
            # Get user's current tokens or guide them to select tokens first
            user_tokens = self.db.get_user_tokens(user_id)
            if not user_tokens:
                logger.warning(f"User {user_id} has no tokens selected for strategy setup")
                await query.edit_message_text(
                    "You need to select which tokens to trade before setting strategies.\n\n"
                    "Please use the button below to select your trading tokens first:",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Select Tokens", callback_data="guide_tokens")]
                    ])
                )
                return ConversationHandler.END
                
            # Display entry strategy selection
            await query.edit_message_text(
                "Let's configure your trading strategies.\n\n"
                f"You're currently trading: *{', '.join(user_tokens)}*\n\n"
                "First, choose your *entry strategy*:\n"
                "(When to enter a position)",
                parse_mode="Markdown",
                reply_markup=self.get_entry_strategy_keyboard()
            )
            
            # Store selected tokens in context for later use
            context.user_data['selected_tokens'] = user_tokens
            
            return CHOOSING_ENTRY_STRATEGY
        except Exception as e:
            logger.error(f"Error in guide_strategies_callback: {str(e)}")
            await query.edit_message_text(
                "Sorry, an error occurred while setting up strategies. Please try again later."
            )
            return ConversationHandler.END
    
    def run(self):
        """Start the bot"""
        logger.info("Starting Abraxas Greenprint Funding Bot")
        self.application.run_polling()
        
if __name__ == '__main__':
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN not set in environment variables")
        exit(1)
        
    bot = AbraxasGreenprintBot(token)
    bot.run()
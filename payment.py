#!/usr/bin/env python3
"""
Production Payment Module for Abraxas Greenprint Funding Bot
----------------------------------------------------------
Handles cryptocurrency payment processing and subscription management with BoomFi
"""

import os
import uuid
import logging
import requests
import json
import base64
import time
from typing import Dict, Optional, List, Any
from datetime import datetime, timedelta
from dotenv import load_dotenv

try:
    from Crypto.PublicKey import RSA
    from Crypto.Signature import PKCS1_v1_5
    from Crypto.Hash import SHA256
except ImportError:
    logging.warning("pycryptodome package not installed. Webhook signature verification will not work.")
    logging.warning("Install with: pip install pycryptodome")

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

class PaymentManager:
    """Handles cryptocurrency payment processing and verification with BoomFi"""
    
    def __init__(self):
        """Initialize payment manager with BoomFi configuration"""
        # BoomFi API configuration
        raw_key = os.getenv("BOOMFI_WEBHOOK_PUBLIC_KEY", "")
        
        # Format the public key properly with header and footer if they're missing
        if raw_key and "-----BEGIN PUBLIC KEY-----" not in raw_key:
            self.boomfi_webhook_public_key = f"-----BEGIN PUBLIC KEY-----\n{raw_key}\n-----END PUBLIC KEY-----"
        else:
            self.boomfi_webhook_public_key = raw_key
        
        # BoomFi payment links for each tier
        self.payment_links = {
            1: os.getenv("BOOMFI_PAYLINK_TIER1", "https://pay.boomfi.xyz/2ujiVa4lkPVCWuTTDuqAOMacbOS"),
            2: os.getenv("BOOMFI_PAYLINK_TIER2", "https://pay.boomfi.xyz/2ujjLRhymjafeE9Dd1uPVfwsu81"),
            3: os.getenv("BOOMFI_PAYLINK_TIER3", "https://pay.boomfi.xyz/2ujjQTamxLv4IPqgMEeBQgFbnkz"),
        }
        
        # Initialize database connection - needed for email lookups
        from database import Database
        self.db = Database()
        
        # Autoconfirm flag for testing (skips real payment processing)
        self.AUTO_APPROVE_PAYMENTS = os.getenv("AUTO_APPROVE_PAYMENTS", "false").lower() == "true"
        
        # Available currencies (supported by BoomFi)
        self.currencies = ['BTC', 'SOL', 'USDC', 'ETH']
        
        # Setup
        self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging for payment manager"""
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
    def get_exchange_rates(self) -> Dict[str, float]:
        """
        Get current exchange rates from a reliable API
        
        Returns:
            Dict mapping currency codes to USD exchange rates
        """
        try:
            # Use CoinGecko API for real-time rates
            response = requests.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params={
                    "ids": "bitcoin,solana,ethereum,usd-coin",
                    "vs_currencies": "usd"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Return rates
                return {
                    'BTC': data.get('bitcoin', {}).get('usd', 50000),
                    'SOL': data.get('solana', {}).get('usd', 100),
                    'ETH': data.get('ethereum', {}).get('usd', 3000),
                    'USDC': 1.0  # Stablecoin pegged to USD
                }
            else:
                logger.error(f"Failed to fetch exchange rates: {response.status_code}")
        except Exception as e:
            logger.error(f"Error fetching exchange rates: {str(e)}")
                
        # Default fallback rates
        return {
            'BTC': 50000,  # Default BTC/USD rate
            'SOL': 100,    # Default SOL/USD rate
            'ETH': 3000,   # Default ETH/USD rate
            'USDC': 1.0    # Stablecoin pegged to USD
        }
        
    def generate_payment_request(self, user_id: int, amount: float, tier: int, 
                               selected_currency: str = "USD") -> Dict[str, Any]:
        """
        Generate a payment request with BoomFi payment link
        
        Args:
            user_id: Telegram user ID
            amount: Payment amount
            tier: Subscription tier
            selected_currency: Currency code (not used with BoomFi payment links)
            
        Returns:
            Dictionary with payment details including checkout URL
        """
        # Generate a unique payment ID
        payment_id = str(uuid.uuid4())
        
        # Log payment request
        logger.info(f"Generating payment request for user {user_id}, tier {tier}, amount {amount} {selected_currency}")
        
        # If auto-approve is enabled, return dummy data
        if self.AUTO_APPROVE_PAYMENTS:
            logger.warning("AUTO_APPROVE_PAYMENTS is enabled, returning dummy checkout data")
            return {
                "payment_id": payment_id,
                "amount": amount,
                "currency": selected_currency,
                "checkout_url": f"https://example.com/dummy-checkout/{payment_id}",
                "success": True,
                "test_mode": True
            }
        
        # Get the payment link for the selected tier
        payment_link = self.payment_links.get(tier)
        if not payment_link:
            logger.error(f"No payment link configured for tier {tier}")
            return {
                "payment_id": payment_id,
                "success": False,
                "error": "Invalid tier selected"
            }
        
        # Add user ID and payment ID to the payment link as query parameters
        checkout_url = f"{payment_link}?user_id={user_id}&payment_id={payment_id}"
        logger.info(f"Generated BoomFi payment link: {checkout_url}")
        
        return {
            "payment_id": payment_id,
            "amount": amount,
            "currency": selected_currency,
            "checkout_url": checkout_url,
            "success": True
        }
    
    def verify_boomfi_signature(self, webhook_data: Dict, signature: str, timestamp: str) -> bool:
        """
        Verify the BoomFi webhook signature using RSA public key verification
        
        Args:
            webhook_data: The webhook payload
            signature: The signature from BoomFi
            timestamp: The timestamp from BoomFi
            
        Returns:
            True if signature is valid, False otherwise
        """
        try:
            # Check if required dependencies are available
            if 'RSA' not in globals():
                logger.error("pycryptodome not installed, cannot verify signatures")
                return False
                
            # Check if public key is available
            if not self.boomfi_webhook_public_key:
                logger.error("Missing BoomFi webhook public key")
                return False
                
            if not signature or not timestamp:
                logger.error("Missing required signature verification components")
                return False
                
            # Log key details for debugging
            key_preview = self.boomfi_webhook_public_key[:30] + "..." if self.boomfi_webhook_public_key else "None"
            logger.info(f"Using public key (preview): {key_preview}")
            
            # Verify the signature is recent (within 5 minutes) to prevent replay attacks
            current_time = int(time.time())
            webhook_time = int(timestamp)
            if abs(current_time - webhook_time) > 300:
                logger.error("Webhook timestamp too old or in the future")
                return False
            
            # Parse the RSA public key
            try:
                public_key = RSA.importKey(self.boomfi_webhook_public_key)
                logger.info("Successfully imported RSA public key")
            except Exception as e:
                logger.error(f"Failed to parse public key: {str(e)}")
                # Log more details about the key format
                logger.error(f"Key format issue. Key length: {len(self.boomfi_webhook_public_key)}, starts with: {self.boomfi_webhook_public_key[:50]}")
                return False
            
            # Create payload string to verify according to BoomFi's documentation:
            # Format: timestamp + "." + body
            payload_str = json.dumps(webhook_data, separators=(',', ':'))
            message = f"{timestamp}.{payload_str}"
            logger.info(f"Verification message format: {timestamp}.<payload>")
            
            # Create a hash of the message
            h = SHA256.new(message.encode('utf-8'))
            
            # Verify the signature
            verifier = PKCS1_v1_5.new(public_key)
            signature_bytes = base64.b64decode(signature)
            verification_result = verifier.verify(h, signature_bytes)
            
            if verification_result:
                logger.info("BoomFi webhook signature verified successfully")
            else:
                logger.warning("BoomFi webhook signature verification failed")
                
            return verification_result
            
        except Exception as e:
            logger.error(f"Error verifying BoomFi signature: {str(e)}")
            # For development/testing, you might want to allow unverified webhooks
            if os.getenv("DEVELOPMENT_MODE", "false").lower() == "true":
                logger.warning("DEVELOPMENT_MODE is enabled, accepting unverified webhook")
                return True
            return False
    
    def process_webhook(self, webhook_data: Dict, headers: Dict) -> Dict:
        """
        Process a BoomFi webhook and update payment status in the database
        
        Args:
            webhook_data: The webhook payload
            headers: The request headers containing signature
            
        Returns:
            Dict containing success status and payment details
        """
        try:
            # Log webhook details
            logger.info(f"Processing BoomFi webhook")
            
            # Get signature and timestamp from headers
            signature = headers.get('X-BoomFi-Signature')
            timestamp = headers.get('X-BoomFi-Timestamp')
            
            # Fallback to lowercase header names if needed
            if not signature:
                signature = headers.get('x-boomfi-signature')
            if not timestamp:
                timestamp = headers.get('x-boomfi-timestamp')
            
            # Verify signature
            if not self.verify_boomfi_signature(webhook_data, signature, timestamp):
                error_msg = "Failed to verify webhook signature"
                logger.error(error_msg)
                # Only enforce signature verification in production
                if os.getenv("DEVELOPMENT_MODE", "false").lower() != "true":
                    return {"success": False, "error": error_msg}
                else:
                    logger.warning("DEVELOPMENT MODE: Continuing despite signature verification failure")
            
            # Extract webhook event and status
            event_type = webhook_data.get('event', '')
            status = webhook_data.get('status', '')
            logger.info(f"Webhook event: {event_type}, status: {status}")
            
            # Check if this is a payment completion webhook
            # According to BoomFi docs, successful payments are "Payment.Updated" events with status "Succeeded"
            if event_type == 'Payment.Updated' and status == 'Succeeded':
                # Extract payment ID
                payment_id = webhook_data.get('id')
                if not payment_id:
                    logger.error("Payment webhook missing payment ID")
                    return {"success": False, "error": "Missing payment ID"}
                
                logger.info(f"Processing successful payment: {payment_id}")
                
                # Extract payment details
                amount = webhook_data.get('amount', '0')
                currency = webhook_data.get('currency', 'USDC')
                
                # Extract plan information to determine tier
                plan = webhook_data.get('plan', {})
                plan_id = plan.get('id', '')
                plan_reference = plan.get('reference', '')
                
                # Extract customer information
                customer = webhook_data.get('customer', {})
                customer_email = customer.get('email', '')
                customer_name = customer.get('name', '')
                
                # Try to determine the tier based on amount or plan reference
                tier = self._determine_tier_from_payment(amount, plan_reference)
                
                # Try to find user by email first
                user_id = None
                if customer_email:
                    logger.info(f"Looking up user by email: {customer_email}")
                    db_user = self.db.get_user_by_email(customer_email)
                    if db_user:
                        user_id = db_user.telegram_id
                        logger.info(f"Found user with Telegram ID {user_id} matching email {customer_email}")
                
                # If no user found by email, try transaction lookup
                if not user_id:
                    transaction = self.db.get_transaction(payment_id)
                    if transaction:
                        # Get user ID from transaction
                        transaction_data = self.db.get_transaction_with_user(payment_id)
                        if transaction_data:
                            user_id = transaction_data.get('user_id')
                            logger.info(f"Found user {user_id} from transaction record")
                
                # If still no user, try extracting from plan reference
                if not user_id:
                    import re
                    user_id_match = re.search(r'user_(\d+)', plan_reference)
                    if user_id_match:
                        user_id = user_id_match.group(1)
                        logger.info(f"Extracted user ID {user_id} from plan reference")
                
                if not user_id:
                    logger.error(f"Could not determine user ID for payment {payment_id}")
                    return {
                        "success": False, 
                        "error": "Could not determine user ID", 
                        "payment_id": payment_id
                    }
                
                # Return success with payment details
                return {
                    "success": True,
                    "payment_id": payment_id,
                    "user_id": user_id,
                    "tier": tier,
                    "status": "completed",
                    "amount": amount,
                    "currency": currency
                }
            else:
                logger.info(f"Ignoring non-completion webhook: {event_type}/{status}")
                return {"success": True, "status": "received"}
            
        except Exception as e:
            logger.error(f"Error processing BoomFi webhook: {str(e)}")
            return {"success": False, "error": str(e)}
            
    def _determine_tier_from_payment(self, amount: str, plan_reference: str) -> int:
        """
        Determine subscription tier from payment amount or plan reference
        
        Args:
            amount: The payment amount as a string
            plan_reference: The plan reference string
            
        Returns:
            Integer tier level (1, 2, or 3)
        """
        # First try to determine tier from plan reference
        plan_reference = plan_reference.lower() if plan_reference else ''
        if 'tier1' in plan_reference or 'test1' in plan_reference:
            logger.info(f"Determined tier 1 from plan reference: {plan_reference}")
            return 1
        elif 'tier2' in plan_reference or 'test2' in plan_reference:
            logger.info(f"Determined tier 2 from plan reference: {plan_reference}")
            return 2
        elif 'tier3' in plan_reference or 'test3' in plan_reference:
            logger.info(f"Determined tier 3 from plan reference: {plan_reference}")
            return 3
            
        # If plan reference doesn't help, try payment amount
        try:
            payment_amount = float(amount)
            if payment_amount <= 5:  # Example price threshold for tier 1 (e.g., test payments)
                tier = 1
            elif payment_amount <= 15:  # Example price threshold for tier 2
                tier = 2
            else:  # Above 15 is tier 3
                tier = 3
                
            logger.info(f"Determined tier {tier} based on payment amount: {payment_amount}")
            return tier
        except (ValueError, TypeError):
            logger.warning(f"Could not parse payment amount: {amount}, defaulting to tier 1")
            return 1  # Default to tier 1
    
    def verify_payment(self, payment_id: str) -> bool:
        """
        Verify if a payment has been completed by checking directly with BoomFi API
        
        Args:
            payment_id: Payment ID to verify
            
        Returns:
            True if payment is completed, False otherwise
        """
        if self.AUTO_APPROVE_PAYMENTS:
            logger.warning(f"AUTO_APPROVE_PAYMENTS is enabled, auto-approving payment {payment_id}")
            return True
            
        # First try to check via BoomFi API (direct verification)
        api_key = os.getenv("BOOMFI_API_KEY")
        if api_key:
            try:
                logger.info(f"Attempting direct API verification for payment {payment_id}")
                
                # BoomFi API base URL
                base_url = "https://api.boomfi.xyz"
                
                # Endpoint to get payment information
                endpoint = f"/v1/payments/{payment_id}"
                
                # Make the API request
                response = requests.get(
                    f"{base_url}{endpoint}",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    payment_data = response.json()
                    
                    # Check payment status (adjust field names based on BoomFi API response structure)
                    payment_status = payment_data.get("status")
                    
                    if payment_status in ["completed", "succeeded", "paid"]:
                        logger.info(f"Payment {payment_id} verified as completed via API")
                        return True
                    else:
                        logger.info(f"Payment {payment_id} status is {payment_status} (not completed)")
                        return False
                else:
                    logger.error(f"Failed to verify payment via API: {response.status_code}")
                    if response.status_code == 404:
                        logger.error(f"Payment {payment_id} not found in BoomFi")
                    elif response.status_code == 401:
                        logger.error("Invalid API key")
                    
                    # Log the error response for debugging
                    try:
                        error_data = response.json()
                        logger.error(f"API error details: {error_data}")
                    except:
                        logger.error(f"API error response: {response.text}")
            except Exception as e:
                logger.error(f"Error calling BoomFi API: {str(e)}")
        else:
            logger.warning("BoomFi API key not configured, cannot perform direct verification")
        
        # If API verification failed or not available, rely on webhooks
        logger.info(f"Falling back to webhook-based verification for payment {payment_id}")
        return False
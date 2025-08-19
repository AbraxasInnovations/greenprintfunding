#!/usr/bin/env python3
"""
Webhook Server for Abraxas Greenprint Funding Bot
---------------------------------------------
Handles BoomFi payment webhook notifications
"""

import os
import logging
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
import time
import re
import requests

from payment import PaymentManager
from database import Database

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize payment manager and database
payment_manager = PaymentManager()
database = Database()

# Get Telegram Bot token from env for direct notifications
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize Firebase for real-time notifications (optional)
try:
    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
    if cred_path:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        logger.info("Firebase initialized for real-time notifications")
    else:
        db = None
        logger.warning("Firebase not initialized - real-time notifications disabled")
except Exception as e:
    db = None
    logger.error(f"Failed to initialize Firebase: {str(e)}")

def notify_user_via_telegram(user_id, tier, payment_id=None):
    """
    Send a direct message to the user through Telegram API
    """
    if not TELEGRAM_BOT_TOKEN:
        logger.error("Cannot send Telegram notification: TELEGRAM_BOT_TOKEN not set")
        return False
        
    try:
        # Use simpler formatting to avoid Markdown parsing errors
        message = (
            "✅ Payment Confirmed!\n\n"
            f"Your Tier {tier} subscription has been activated successfully.\n\n"
            "Let's set up your trading bot in a few easy steps:\n\n"
            "1. Select tokens to trade (required)\n"
            "2. Configure entry & exit strategies\n"
            "3. Configure your exchange API keys (required)\n"
            "4. Start your trading bot"
        )
        
        # Add inline keyboard buttons to guide the user through setup
        keyboard = {
            "inline_keyboard": [
                [{"text": "🪙 Step 1: Select Tokens", "callback_data": "guide_tokens"}],
                [{"text": "📊 Step 2: Set Strategies", "callback_data": "guide_strategies"}],
                [{"text": "🔑 Step 3: Set API Keys", "callback_data": "guide_keys"}]
            ]
        }
        
        telegram_api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": user_id,
            "text": message,
            "parse_mode": "",
            "reply_markup": json.dumps(keyboard)
        }
        
        logger.info(f"Sending notification to user {user_id} with message: {message[:50]}...")
        response = requests.post(telegram_api_url, json=payload)
        
        if response.status_code == 200:
            logger.info(f"Telegram notification sent to user {user_id}")
            return True
        else:
            logger.error(f"Failed to send Telegram notification: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending Telegram notification: {str(e)}")
        return False

@app.route('/webhook/boomfi', methods=['POST'])
def boomfi_webhook():
    """Handle BoomFi webhook notifications"""
    try:
        # Full request debugging
        logger.info("==== WEBHOOK RECEIVED ====")
        
        # Log all headers
        logger.info("==== HEADERS ====")
        for header_name, header_value in request.headers.items():
            logger.info(f"{header_name}: {header_value}")
        
        # Get raw request body
        raw_data = request.get_data(as_text=True)
        logger.info(f"==== RAW REQUEST BODY ====\n{raw_data}")
        
        # Parse JSON
        try:
            webhook_data = request.json
            logger.info(f"==== PARSED JSON ====\n{json.dumps(webhook_data, indent=2)}")
        except Exception as e:
            logger.error(f"Failed to parse JSON: {str(e)}")
            return jsonify({"status": "error", "message": "Invalid JSON format"}), 400
        
        if not webhook_data:
            logger.error("Received empty webhook from BoomFi")
            return jsonify({"status": "error", "message": "Empty webhook data"}), 400
        
        # Development mode - bypass signature verification for testing
        development_mode = os.getenv("DEVELOPMENT_MODE", "false").lower() == "true"
        if development_mode:
            logger.warning("DEVELOPMENT MODE: Bypassing signature verification")
        else:
            # Verify signature in production mode
            signature = request.headers.get('X-BoomFi-Signature')
            timestamp = request.headers.get('X-BoomFi-Timestamp')
            
            if not signature or not timestamp:
                logger.error("Missing required headers for signature verification")
                return jsonify({"status": "error", "message": "Missing required headers"}), 400
                
            if not payment_manager.verify_boomfi_signature(webhook_data, signature, timestamp):
                logger.error("Invalid webhook signature")
                return jsonify({"status": "error", "message": "Invalid signature"}), 401
            
        # Extract event type and status
        event = webhook_data.get('event', '')
        status = webhook_data.get('status', '')
        
        logger.info(f"Event: {event}, Status: {status}")
        
        if event == 'Payment.Updated' and status == 'Succeeded':
            logger.info("Detected successful payment")
            
            # Extract payment details
            payment_id = webhook_data.get('id')
            
            # Extract amount and currency
            amount = webhook_data.get('amount', '0')
            currency = webhook_data.get('currency', 'USDC')
            logger.info(f"Payment amount: {amount} {currency}")
            
            # Extract plan information
            plan = webhook_data.get('plan', {})
            plan_id = plan.get('id', '')
            plan_reference = plan.get('reference', '')
            logger.info(f"Plan ID: {plan_id}, Reference: {plan_reference}")
            
            # Extract customer information
            customer = webhook_data.get('customer', {})
            customer_id = customer.get('id', '')
            customer_email = customer.get('email', '')
            customer_name = customer.get('name', '')
            logger.info(f"Customer: {customer_name} ({customer_email}), ID: {customer_id}")
            
            # Determine the subscription tier based on the payment amount
            try:
                payment_amount = float(amount)
                # Use exact price matching for tiers
                if payment_amount == 49.0:  # Tier 1 price
                    tier = 1
                elif payment_amount == 1.27:  # Tier 2 price
                    tier = 2
                elif payment_amount == 2500.0:  # Tier 3 price
                    tier = 3
                else:
                    # Log unexpected amount and default to tier based on ranges
                    logger.warning(f"Unexpected payment amount: {payment_amount}. Using range-based tier determination.")
                    if payment_amount < 70:  # Up to $70 is tier 1
                        tier = 1
                    elif payment_amount < 1000:  # Up to $1000 is tier 2
                        tier = 2
                    else:  # Above $1000 is tier 3
                        tier = 3
                
                logger.info(f"Determined tier {tier} based on payment amount: {payment_amount}")
            except (ValueError, TypeError):
                logger.error(f"Could not parse payment amount: {amount}")
                return jsonify({"status": "error", "message": "Invalid payment amount"}), 400
            
            # Try to find user by email first
            user_id = None
            if customer_email:
                logger.info(f"Looking up user by email: {customer_email}")
                db_user = database.get_user_by_email(customer_email)
                if db_user:
                    user_id = db_user.telegram_id
                    logger.info(f"Found user with Telegram ID {user_id} matching email {customer_email}")
            
            # If we still don't have a user ID, try to extract from URL parameters
            if not user_id:
                try:
                    # Look for user ID in payment data or URL
                    payment_data = webhook_data.get('metadata', {})
                    user_id = payment_data.get('telegram_id')
                    if not user_id:
                        # Try to extract from success URL
                        success_url = webhook_data.get('success_url', '')
                        user_id_match = re.search(r'user_id=(\d+)', success_url)
                        if user_id_match:
                            user_id = int(user_id_match.group(1))
                            logger.info(f"Extracted user ID {user_id} from success URL")
                except Exception as e:
                    logger.error(f"Error extracting user ID: {str(e)}")
            
            if not user_id:
                logger.error("Could not determine user ID from webhook data")
                return jsonify({"status": "error", "message": "User ID not found"}), 400
            
            # Update transaction in database
            try:
                # First check if transaction exists
                transaction = database.get_transaction(payment_id)
                if not transaction:
                    # Create new transaction if it doesn't exist
                    logger.info(f"Creating new transaction for payment {payment_id}")
                    transaction = database.create_transaction(
                        user_id=user_id,
                        amount=float(amount),
                        tier=tier,
                        transaction_id=payment_id,
                        payment_data=json.dumps(webhook_data)
                    )
                    if not transaction:
                        logger.error(f"Failed to create transaction for payment {payment_id}")
                        return jsonify({"status": "error", "message": "Failed to create transaction"}), 500
                
                # Update transaction status
                success = database.update_transaction_status(payment_id, 'completed')
                if not success:
                    logger.error(f"Failed to update transaction status for payment {payment_id}")
                    return jsonify({"status": "error", "message": "Failed to update transaction"}), 500
                
                # Update user's subscription
                from datetime import datetime, timedelta
                expiry_date = datetime.now() + timedelta(days=30)
                success = database.update_user_subscription(
                    telegram_id=user_id,
                    tier=tier,
                    expiry=expiry_date
                )
                if not success:
                    logger.error(f"Failed to update subscription for user {user_id}")
                    return jsonify({"status": "error", "message": "Failed to update subscription"}), 500
                
                # Verify the subscription update
                user = database.get_user_by_telegram_id(user_id)
                if not user or user.subscription_tier != tier:
                    logger.error(f"Subscription verification failed. Expected tier {tier}, got {user.subscription_tier if user else 'None'}")
                    return jsonify({"status": "error", "message": "Subscription verification failed"}), 500
                
                logger.info(f"Successfully updated subscription for user {user_id} to tier {tier}")
                
            except Exception as e:
                logger.error(f"Database error: {str(e)}")
                return jsonify({"status": "error", "message": "Database error"}), 500
            
            # Send notification to user
            try:
                notify_user_via_telegram(user_id, tier, payment_id)
            except Exception as e:
                logger.error(f"Failed to send notification: {str(e)}")
                # Don't return error here, as the payment was still processed successfully
            
            return jsonify({"status": "success", "message": "Payment processed successfully"}), 200
        
        else:
            logger.info(f"Ignoring non-payment or non-success event: {event} - {status}")
            return jsonify({"status": "success", "message": "Event ignored"}), 200
        
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/webhook/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok"}), 200

@app.route('/webhook/test', methods=['GET'])
def test_webhook():
    """Test endpoint to manually trigger a payment completion"""
    try:
        user_id = request.args.get('user_id', '1234567890')  # Default to test user ID
        payment_id = request.args.get('payment_id', f"test_{int(time.time())}")
        tier = request.args.get('tier', '1')
        
        logger.info(f"Test webhook triggered for user {user_id}, payment {payment_id}, tier {tier}")
        
        # Update transaction status
        database.update_transaction_status(payment_id, 'completed')
        
        # Update user subscription (30 days from now)
        from datetime import datetime, timedelta
        database.update_user_subscription(
            telegram_id=int(user_id),
            tier=int(tier),
            expiry=datetime.now() + timedelta(days=30)
        )
        
        logger.info(f"Test payment completed for user {user_id}, tier {tier}. Subscription updated.")
        
        # Send direct notification to the user's Telegram chat for test payments too
        notify_user_via_telegram(user_id, tier, payment_id)
        
        return jsonify({
            "status": "success",
            "message": "Test payment processed successfully",
            "user_id": user_id,
            "tier": tier,
            "payment_id": payment_id
        }), 200
    except Exception as e:
        logger.error(f"Error processing test webhook: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/webhook/test_notification', methods=['GET'])
def test_notification():
    """Test endpoint to try sending a notification to a specific user"""
    try:
        user_id = request.args.get('user_id')
        tier = request.args.get('tier', '1')
        
        if not user_id:
            return jsonify({
                "status": "error",
                "message": "Missing user_id parameter"
            }), 400
            
        logger.info(f"Testing notification for user {user_id}, tier {tier}")
        
        # Send notification
        notification_sent = notify_user_via_telegram(user_id, tier, "test_payment")
        
        if notification_sent:
            return jsonify({
                "status": "success",
                "message": f"Test notification sent to user {user_id}"
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": f"Failed to send notification to user {user_id}"
            }), 500
            
    except Exception as e:
        logger.error(f"Error sending test notification: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error: {str(e)}"
        }), 500

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.getenv("PORT", 80))
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=port, debug=False) 
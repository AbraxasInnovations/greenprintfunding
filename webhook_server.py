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
            
            # Extract event type and status
            event = webhook_data.get('event', '')
            status = webhook_data.get('status', '')
            
            logger.info(f"Event: {event}, Status: {status}")
            
            # Check if this is a successful payment
            # According to BoomFi docs, successful payments are "Payment.Updated" events with status "Succeeded"
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
                
                # Try to determine the subscription tier based on the payment amount
                tier = 1  # Default to tier 1
                
                # Price-based tier determination
                try:
                    payment_amount = float(amount)
                    if payment_amount <= 5:  # Example price threshold for tier 1 (e.g., test payments)
                        tier = 1
                    elif payment_amount <= 15:  # Example price threshold for tier 2
                        tier = 2
                    else:  # Above 15 is tier 3
                        tier = 3
                    
                    logger.info(f"Determined tier {tier} based on payment amount: {payment_amount}")
                except (ValueError, TypeError):
                    logger.warning(f"Could not parse payment amount: {amount}")
                
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
                    # Try to extract from payment_id or plan_reference
                    user_id_match = re.search(r'user_id=(\d+)', plan_reference)
                    if user_id_match:
                        user_id = int(user_id_match.group(1))
                        logger.info(f"Extracted user ID {user_id} from plan reference")
                
                # For testing, use a hardcoded test user ID if no user was found
                if not user_id:
                    # IMPORTANT: Replace this with your actual Telegram ID for testing
                    user_id = 1234567890
                    logger.warning(f"No user found for email {customer_email}. Using fallback user ID {user_id} for testing!")
                
                # If we have the necessary details, process the payment
                if user_id and payment_id:
                    try:
                        # Update transaction status
                        logger.info(f"Updating transaction for {payment_id}")
                        database.update_transaction_status(payment_id, 'completed')
                        
                        # Update user subscription (30 days from now)
                        from datetime import datetime, timedelta
                        logger.info(f"Updating subscription for user {user_id}, tier {tier}")
                        database.update_user_subscription(
                            telegram_id=int(user_id),
                            tier=int(tier),
                            expiry=datetime.now() + timedelta(days=30)
                        )
                        
                        logger.info(f"Payment completed for user {user_id}, tier {tier}")
                        
                        # Send direct notification to the user's Telegram chat
                        notify_user_via_telegram(user_id, tier, payment_id)
                        
                        # Notify user via Firebase (if available)
                        if db:
                            try:
                                db.collection('notifications').add({
                                    'user_id': int(user_id),
                                    'type': 'payment_completed',
                                    'payment_id': payment_id,
                                    'tier': int(tier),
                                    'timestamp': firestore.SERVER_TIMESTAMP
                                })
                                logger.info(f"Added Firebase notification for user {user_id}")
                            except Exception as e:
                                logger.error(f"Failed to add Firebase notification: {str(e)}")
                        
                        # Return a more detailed success response
                        return jsonify({
                            "status": "success", 
                            "message": "Payment completed successfully",
                            "user_id": user_id,
                            "tier": tier,
                            "payment_id": payment_id,
                            "amount": amount,
                            "currency": currency
                        }), 200
                    except Exception as e:
                        logger.error(f"Error processing payment: {str(e)}")
                        # Return generic success to BoomFi but log the error
                        return jsonify({
                            "status": "success", 
                            "message": "Webhook received but processing encountered an error"
                        }), 200
                else:
                    logger.error(f"Missing required data for payment processing: user_id={user_id}, payment_id={payment_id}")
            else:
                logger.info(f"Not a successful payment event/status: {event}/{status}")
            
            # Return generic success for other events
            return jsonify({
                "status": "success", 
                "message": "Webhook received"
            }), 200
                    
        # Normal processing with signature verification
        # Get headers for signature verification
        headers = request.headers
        
        # BoomFi signature headers
        signature = headers.get('X-BoomFi-Signature')
        timestamp = headers.get('X-BoomFi-Timestamp')
        
        # If headers are missing, try lowercase versions (for consistency)
        if not signature:
            signature = headers.get('x-boomfi-signature')
        if not timestamp:
            timestamp = headers.get('x-boomfi-timestamp')
            
        # Log signature information
        if signature and timestamp:
            logger.info(f"Webhook signature present. Timestamp: {timestamp}")
        else:
            logger.warning("Webhook signature missing or incomplete")
        
        # Process the webhook data
        result = payment_manager.process_webhook(webhook_data, headers)
        
        if not result.get('success'):
            logger.error(f"Failed to process webhook: {result.get('error')}")
            return jsonify({"status": "error", "message": result.get('error')}), 400
        
        # Get payment details
        payment_id = result.get('payment_id')
        user_id = result.get('user_id')
        tier = result.get('tier')
        status = result.get('status')
        
        logger.info(f"Payment {payment_id} status: {status}, User: {user_id}, Tier: {tier}")
        
        # Update transaction status in database
        if status == 'completed':
            # Update transaction status
            database.update_transaction_status(payment_id, 'completed')
            
            # Update user subscription (30 days from now)
            from datetime import datetime, timedelta
            database.update_user_subscription(
                telegram_id=int(user_id),
                tier=int(tier),
                expiry=datetime.now() + timedelta(days=30)
            )
            
            logger.info(f"Payment completed for user {user_id}, tier {tier}. Subscription updated.")
            
            # Send direct notification to the user's Telegram chat
            notify_user_via_telegram(user_id, tier, payment_id)
            
            # Notify user via Firebase (if available)
            if db:
                try:
                    db.collection('notifications').add({
                        'user_id': int(user_id),
                        'type': 'payment_completed',
                        'payment_id': payment_id,
                        'tier': int(tier),
                        'timestamp': firestore.SERVER_TIMESTAMP
                    })
                    logger.info(f"Added Firebase notification for user {user_id}")
                except Exception as e:
                    logger.error(f"Failed to add Firebase notification: {str(e)}")
            
            # Return a more detailed success response
            return jsonify({
                "status": "success", 
                "message": "Payment completed successfully",
                "user_id": user_id,
                "tier": tier,
                "payment_id": payment_id
            }), 200
        
        # Return success response
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.error(f"Error processing BoomFi webhook: {str(e)}")
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
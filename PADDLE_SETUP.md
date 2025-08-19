# Paddle Payment Integration Setup

This document provides instructions for setting up Paddle as the payment provider for the Abraxas Greenprint Funding Bot.

## Prerequisites

1. Sign up for a Paddle account at [paddle.com](https://paddle.com)
2. Create products in Paddle for each subscription tier:
   - Tier 1: $50/month
   - Tier 2: $100/month
   - Tier 3: $200/month

## Configuration Steps

### 1. Get Paddle API Credentials

1. Login to your Paddle dashboard
2. Go to Developer Tools > Authentication
3. Get your Vendor ID and API Key
4. Generate a webhook secret

### 2. Create Products in Paddle

1. Go to Catalog > Products
2. Create a separate product for each tier with the appropriate pricing
3. Note down the product IDs for each tier

### 3. Set Up Webhook

1. In Paddle dashboard, go to Developer Tools > Webhooks
2. Add a new webhook with the following settings:
   - URL: `https://your-domain.com/webhook/paddle` (replace with your actual domain)
   - Events to subscribe to:
     - `payment_succeeded`
     - `payment_refunded`
     - `payment_disputed`
3. Make sure your webhook endpoint is publicly accessible

### 4. Update Environment Variables

Update your `.env` file with the following variables:

```
PADDLE_VENDOR_ID=your_paddle_vendor_id
PADDLE_API_KEY=your_paddle_api_key
PADDLE_PUBLIC_KEY=your_paddle_public_key
PADDLE_WEBHOOK_SECRET=your_paddle_webhook_secret
PADDLE_PRODUCT_TIER1=product_id_for_tier1
PADDLE_PRODUCT_TIER2=product_id_for_tier2
PADDLE_PRODUCT_TIER3=product_id_for_tier3
PADDLE_TEST_MODE=true  # Set to false in production
WEBHOOK_URL=https://your-domain.com/webhook/paddle
```

### 5. Deploy Webhook Server

The webhook server needs to be accessible from the internet. You can deploy it using:

```bash
python webhook_server.py
```

For production, consider running it with a WSGI server like gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 webhook_server:app
```

Make sure to set up proper SSL/TLS if you're deploying to production.

## Testing

1. Set `PADDLE_TEST_MODE=true` in your `.env` file
2. Run your bot and go through the subscription process
3. When you click "Pay Now", you should be redirected to Paddle's checkout page
4. Complete the checkout using Paddle's test payment methods:
   - Credit Card: 4242 4242 4242 4242, any future expiry date, any CVC
5. After payment, you should be redirected back to the bot
6. Check your webhook server logs to ensure the webhook is being received

## Troubleshooting

### Payment Webhooks Not Received

1. Verify your webhook URL is publicly accessible
2. Check webhook logs in the Paddle dashboard
3. Ensure your webhook server is running and accessible

### Users Not Redirected After Payment

1. Verify the return URL is correct in the payment request
2. Check that your bot is correctly handling the payment confirmation callback

### Testing / Development

For local testing without a public server, you can set:

```
AUTO_APPROVE_PAYMENTS=true
```

This will auto-approve payments without requiring Paddle integration, but should not be used in production. 
#!/usr/bin/env python3
"""
Clean implementation of the handle_webhook method for the Abraxas Greenprint Funding Bot
"""

import logging
from aiohttp import web
from telegram import Update

logger = logging.getLogger(__name__)

class WebhookHandler:
    def __init__(self, application):
        self.application = application

    async def handle_webhook(self, request):
        """Handle incoming webhook updates."""
        try:
            # Get the update from the request
            data = await request.json()
            logger.info(f"Received webhook update: {data}")
            
            # Process the update
            update = Update.de_json(data, self.application.bot)
            await self.application.process_update(update)
            
            return web.Response(text="OK")
        except Exception as e:
            logger.error(f"Error processing webhook update: {str(e)}", exc_info=True)
            return web.Response(text="Error", status=500) 
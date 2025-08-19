#!/usr/bin/env python3
"""
Test script for Hyperliquid WebSocket allMids subscription
This script connects to the Hyperliquid WebSocket and subscribes to allMids
to see what tokens are available without authentication.
"""

import json
import websocket
import threading
import time
import sys

class HyperliquidTester:
    def __init__(self):
        self.hl_ws_url = "wss://api.hyperliquid.xyz/ws"
        self.ws = None
        self.running = True
        self.debug_logged = False
        self.all_mids_data = None
        
    def on_message(self, ws, message):
        """Handle WebSocket messages"""
        try:
            data = json.loads(message)
            print(f"\nReceived message from channel: {data.get('channel', 'unknown')}")
            
            # For allMids data, store and process it
            if data.get('channel') == 'allMids':
                self.all_mids_data = data.get('data', [])
                if self.all_mids_data:
                    print("\nAvailable tokens from allMids:")
                    # Extract and print tokens from the data
                    tokens = [item.get('coin') for item in self.all_mids_data if 'coin' in item]
                    for token in tokens:
                        print(f"- {token}")
                    print(f"\nTotal tokens available: {len(tokens)}")
                else:
                    print("No token data received in allMids message")
            
            # For the first few messages, print the full structure for debugging
            if not self.debug_logged or (data.get('channel') == 'allMids' and not self.all_mids_data):
                print("\nDEBUG: Full WebSocket Message Structure:")
                print(json.dumps(data, indent=2))
                self.debug_logged = True
                
        except Exception as e:
            print(f"Error processing WebSocket message: {e}")
            print(f"Raw message: {message}")
    
    def on_error(self, ws, error):
        print(f"WebSocket error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print(f"WebSocket closed: {close_status_code=}, {close_msg=}")
        if self.running:
            print("Attempting to reconnect...")
            time.sleep(2)
            self.connect_websocket()

    def on_open(self, ws):
        print("WebSocket connected")
        # Subscribe to allMids as per documentation
        subscribe_msg = {
            "method": "subscribe",
            "subscription": {
                "type": "allMids"
            }
        }
        ws.send(json.dumps(subscribe_msg))
        print("Subscribed to allMids feed")
    
    def connect_websocket(self):
        """Connect to WebSocket with auto-reconnect"""
        print(f"Connecting to {self.hl_ws_url}...")
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
    
    def run(self):
        """Main test loop"""
        print("Starting Hyperliquid WebSocket allMids test...")
        self.connect_websocket()
        
        # Wait for connection and data
        wait_time = 0
        max_wait = 20  # Maximum wait time in seconds
        
        print("\nWaiting for data...")
        try:
            while self.running and wait_time < max_wait:
                if self.all_mids_data:
                    print("\nReceived allMids data successfully!")
                    break
                time.sleep(1)
                wait_time += 1
                sys.stdout.write(".")
                sys.stdout.flush()
            
            if wait_time >= max_wait and not self.all_mids_data:
                print("\nTimed out waiting for allMids data")
            
            print("\nKeeping connection open to receive updates...")
            print("Press Ctrl+C to exit")
            
            # Keep running until interrupted
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\nShutting down tester...")
            self.running = False
        finally:
            if self.ws:
                self.ws.close()

def main():
    tester = HyperliquidTester()
    tester.run()

if __name__ == "__main__":
    main() 
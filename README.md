# Crypto Funding Rate Arbitrage Bot

## Overview

This Python bot is designed to execute funding rate arbitrage strategies between Kraken (spot) and Hyperliquid (perpetual futures). It monitors funding rates on Hyperliquid and aims to capture positive funding by simultaneously shorting perpetual contracts on Hyperliquid and buying the equivalent amount on Kraken's spot market.

## Key Features

*   **Multi-Exchange:** Operates between Kraken (spot) and Hyperliquid (perps).
*   **Multi-Asset:** Capable of trading multiple configured cryptocurrency assets simultaneously (depending on Tier).
*   **Dynamic Position Sizing:** Calculates trade sizes based on available capital, asset margin requirements, and configured tier strategy.
*   **Tiered Allocation Strategy:**
    *   **Tier 1:** Trades only the single highest-yielding configured asset.
    *   **Tier 2/3:** Allocates capital proportionally to positive funding rates across multiple configured assets, with a pivot mechanism to focus capital if minimum order sizes aren't met for all allocated assets.
*   **Configurable Strategies:** Entry and Exit conditions (percentile thresholds, time-based exits using predicted rates) can be configured.
*   **WebSocket Integration:** Uses WebSockets for real-time funding rate and market data updates from Hyperliquid.
*   **Robust API Interaction:** Includes rate limiting, retries, and error handling for both Kraken and Hyperliquid API calls.
*   **Safety Mechanisms:** Implements margin level checks and emergency position closing capabilities. Flash crash protection is included but requires integration into the main loop.

## Current Status & Progress (MVP Focus)

*   **Core Logic:** Significant refactoring completed to implement dynamic sizing, tier logic, and robust helper methods for API interaction and order management based on successful patterns from simpler bots.
*   **WebSocket:** Configured to subscribe to `activeAssetCtx` for real-time funding rates and `webData2` for positions/margin, processing messages in a separate thread.
*   **Order Execution:** `place_hl_order`, `place_kraken_order`, `wait_for_..._fill`, `cancel_..._order`, `close_hl_position`, etc., have been implemented/refactored to use limit orders, handle retries, wait for fills, and verify positions.
*   **Orchestration:** `enter_positions` and `exit_positions` have been refactored to manage the two legs of the trade atomically, handle failures, and attempt reverts.
*   **Safety:** `check_margin_levels` and `emergency_close_all_positions` are implemented. `check_for_flash_crash` is implemented but needs integration.
*   **State:** Uses a multi-asset dictionary (`self.assets`) and threading lock (`self.lock`) for managing state.

**This bot is currently considered an MVP (Minimum Viable Product). Further testing and potentially refinement are required before deploying with significant capital.**

## Setup

1.  **Configuration File:**
    *   Create a `user_config.ini` file (or specify a different path) in the same directory.
    *   Populate it with your API keys and secrets for Kraken and Hyperliquid (using the private key for HL signing). Include your HL wallet address.
    *   Define selected tokens and entry/exit strategies under `[Strategies]` and `[tokens]` sections if desired (defaults will be used otherwise). See example below.
    *   Example `user_config.ini`:
        ```ini
        [kraken]
        api_key = YOUR_KRAKEN_API_KEY
        api_secret = YOUR_KRAKEN_SECRET

        [hyperliquid]
        # api_key = YOUR_HL_API_KEY_OPTIONAL
        private_key = YOUR_HL_PRIVATE_KEY_0x...
        wallet_address = YOUR_HL_WALLET_ADDRESS_0x...

        [Strategies]
        # Examples: default, 50, 75, 85, 95, abraxas
        entry_strategy = default
        # Examples: default, 50, 35, 20, 10, exit_abraxas
        exit_strategy = default

        # Optional: Define specific tokens to trade if overriding class defaults
        # [tokens]
        # selected = BTC,ETH,SOL
        ```
2.  **Trading Pairs:**
    *   Ensure a `trading_pairs.py` file exists in the same directory.
    *   This file must define a dictionary named `AVAILABLE_PAIRS`.
    *   Each key in `AVAILABLE_PAIRS` should be the uppercase asset symbol (e.g., 'BTC').
    *   The value for each key should be another dictionary containing specifications like `margin_size`, `kraken_pair`, `price_precision`, etc.
3.  **Environment:**
    *   Set up a Python 3 environment.
    *   Install required libraries: `requests`, `websocket-client`, `pandas`, `numpy`, `pytz`, `hyperliquid-python-sdk`, `eth_account`, `web3` (likely a dependency of `eth_account`).
    *   A `requirements.txt` file should ideally be created and maintained. `pip install -r requirements.txt`

## How to Run

1.  Ensure your `user_config.ini` and `trading_pairs.py` are correctly configured.
2.  Select the appropriate Bot Tier class (Tier1Bot, Tier2Bot, Tier3Bot) in the `if __name__ == '__main__':` block of `arb_bot.py`.
3.  Define the `selected_tokens` list for the chosen tier instance.
4.  Run the bot from your terminal:
    ```bash
    python arb_bot.py
    ```
5.  Monitor the logs (`arb_bot_<user_id>.log`) closely.

## Important Notes & Warnings

*   **MVP STATUS:** This code requires thorough testing in a safe environment (e.g., with minimal capital) before live deployment. Bugs may still exist.
*   **RISK:** Trading cryptocurrencies involves significant risk. This bot automates trading decisions and can lose money rapidly. Use at your own risk. Understand the code completely before running it.
*   **MARGIN CALCULATION:** The `check_margin_levels` implementation uses an assumed formula. **Verify the correct margin calculation based on official Hyperliquid documentation** and update the code if necessary.
*   **CONFIGURATION:** Ensure all parameters in `__init__` and the `.ini` file are set appropriately for your risk tolerance and exchange limits.
*   **API KEYS:** Securely manage your API keys and private keys. Do not commit them to version control.

## TODO / Next Steps

*   Integrate `check_for_flash_crash` calls into the main loop/message processing.
*   Integrate `is_flash_crash_cooldown_active` check into `evaluate_and_execute_trades`.
*   Thoroughly test entry/exit logic, especially failure and revert scenarios.
*   Add querying of HL fills to get accurate average fill prices for the HL leg (currently estimated).
*   Implement more granular error handling in orchestrator methods.
*   Consider adding external monitoring and alerting (e.g., via Telegram).
*   Create and maintain `requirements.txt`.
*   Add unit and integration tests. 
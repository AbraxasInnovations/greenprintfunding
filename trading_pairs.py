#!/usr/bin/env python3
"""
Trading Pairs Module for Abraxas Greenprint Funding Bot
----------------------------------------------------
Defines available trading pairs and validation functions
"""

import requests
import logging
from typing import List, Dict, Set, Tuple, Optional

# Configure logging
logger = logging.getLogger(__name__)

AVAILABLE_PAIRS = {
    "HPOS": {
        "description": "Harry Potter OSI10 - Available on both Hyperliquid and Kraken",
        "kraken_pair": "HPOS10IUSD",
        "hl_order_type": "market",
        "price_precision": 2,
        "position_size": 12.0,
        "margin_size": 4.0,
    },
    "BADGER": {
        "description": "Badger DAO - Available on both Hyperliquid and Kraken",
        "kraken_pair": "BADGERUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0,
    },
    "BTC": {
        "description": "Bitcoin - Available on both Hyperliquid and Kraken",
        "kraken_pair": "XXBTZUSD",
        "hl_order_type": "limit",
        "price_precision": 1,
        "position_size": 12.0,
        "margin_size": 4.0,
    },
    "ETH": {
        "description": "Ethereum - Available on both Hyperliquid and Kraken",
        "kraken_pair": "XETHZUSD",
        "hl_order_type": "limit",
        "price_precision": 2,
        "position_size": 12.0,
        "margin_size": 4.0,
    },
    "HYPE": {
        "description": "Hyperliquid token - Special case: both perp and spot on Hyperliquid",
        "kraken_pair": None,  # No Kraken pair needed
        "hyperliquid_spot": True,  # Flag indicating spot is on Hyperliquid
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0,
    },
    "ADA": {
        "description": "ADA - Available on Kraken",
        "kraken_pair": "ADAUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "AI16Z": {
        "description": "AI16Z - Available on Kraken",
        "kraken_pair": "AI16ZUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "AIXBT": {
        "description": "AIXBT - Available on Kraken",
        "kraken_pair": "AIXBTUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "ALGO": {
        "description": "ALGO - Available on Kraken",
        "kraken_pair": "ALGOUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "ALT": {
        "description": "ALT - Available on Kraken",
        "kraken_pair": "ALTUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "AAVE": {
        "description": "AAVE - Available on Kraken",
        "kraken_pair": "AAVEUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "APE": {
        "description": "APE - Available on Kraken",
        "kraken_pair": "APEUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "APT": {
        "description": "APT - Available on Kraken",
        "kraken_pair": "APTUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "ATOM": {
        "description": "ATOM - Available on Kraken",
        "kraken_pair": "ATOMUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "AVAX": {
        "description": "AVAX - Available on Kraken",
        "kraken_pair": "AVAXUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "BERA": {
        "description": "BERA - Available on Kraken",
        "kraken_pair": "BERAUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "BIGTIME": {
        "description": "BIGTIME - Available on Kraken",
        "kraken_pair": "BIGTIMEUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "BIO": {
        "description": "BIO - Available on Kraken",
        "kraken_pair": "BIOUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "BLUR": {
        "description": "BLUR - Available on Kraken",
        "kraken_pair": "BLURUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "BNT": {
        "description": "BNT - Available on Kraken",
        "kraken_pair": "BNTUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "CRV": {
        "description": "CRV - Available on Kraken",
        "kraken_pair": "CRVUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "CYBER": {
        "description": "CYBER - Available on Kraken",
        "kraken_pair": "CYBERUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "DYDX": {
        "description": "DYDX - Available on Kraken",
        "kraken_pair": "DYDXUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "DYM": {
        "description": "DYM - Available on Kraken",
        "kraken_pair": "DYMUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "DOT": {
        "description": "Polkadot - Available on Kraken",
        "kraken_pair": "DOTUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "EIGEN": {
        "description": "EIGEN - Available on Kraken",
        "kraken_pair": "EIGENUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "ENA": {
        "description": "ENA - Available on Kraken",
        "kraken_pair": "ENAUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "ENS": {
        "description": "ENS - Available on Kraken",
        "kraken_pair": "ENSUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "ETC": {
        "description": "ETC - Available on Kraken (as XETCZ)",
        "kraken_pair": "XETCZUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "ETHFI": {
        "description": "ETHFI - Available on Kraken",
        "kraken_pair": "ETHFIUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "FET": {
        "description": "FET - Available on Kraken",
        "kraken_pair": "FETUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "FIL": {
        "description": "FIL - Available on Kraken",
        "kraken_pair": "FILUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "FXS": {
        "description": "FXS - Available on Kraken",
        "kraken_pair": "FXSUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "GALA": {
        "description": "GALA - Available on Kraken",
        "kraken_pair": "GALAUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "GRASS": {
        "description": "GRASS - Available on Kraken",
        "kraken_pair": "GRASSUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "GRIFFAIN": {
        "description": "GRIFFAIN - Available on Kraken",
        "kraken_pair": "GRIFFAINUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "HPOS": {
        "description": "Harry Potter OSI10 - Available on both Hyperliquid and Kraken",
        "kraken_pair": "HPOS10IUSD",
        "hl_order_type": "market",
        "price_precision": 2,
        "position_size": 12.0,
        "margin_size": 4.0,
    },
    "INJ": {
        "description": "INJ - Available on Kraken",
        "kraken_pair": "INJUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "JUP": {
        "description": "JUP - Available on Kraken",
        "kraken_pair": "JUPUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "KAITO": {
        "description": "KAITO - Available on Kraken",
        "kraken_pair": "KAITOUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "KAS": {
        "description": "KAS - Available on Kraken",
        "kraken_pair": "KASUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "LINK": {
        "description": "LINK - Available on Kraken",
        "kraken_pair": "LINKUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "ME": {
        "description": "ME - Available on Kraken",
        "kraken_pair": "MEUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "MEME": {
        "description": "MEME - Available on Kraken",
        "kraken_pair": "MEMEUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "MINA": {
        "description": "MINA - Available on Kraken",
        "kraken_pair": "MINAUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "MNT": {
        "description": "MNT - Available on Kraken",
        "kraken_pair": "MNTUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "MOODENG": {
        "description": "MOODENG - Available on Kraken",
        "kraken_pair": "MOODENGUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "MORPHO": {
        "description": "MORPHO - Available on Kraken",
        "kraken_pair": "MORPHOUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "MOVE": {
        "description": "MOVE - Available on Kraken",
        "kraken_pair": "MOVEUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "MEW": {
        "description": "MEW - Available on Kraken",
        "kraken_pair": "MEWUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "NEAR": {
        "description": "NEAR - Available on Kraken",
        "kraken_pair": "NEARUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "NOT": {
        "description": "NOT - Available on Kraken",
        "kraken_pair": "NOTUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "NTRN": {
        "description": "NTRN - Available on Kraken",
        "kraken_pair": "NTRNUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "OM": {
        "description": "OM - Available on Kraken",
        "kraken_pair": "OMUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "ONDO": {
        "description": "ONDO - Available on Kraken",
        "kraken_pair": "ONDOUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "PENDLE": {
        "description": "PENDLE - Available on Kraken",
        "kraken_pair": "PENDLEUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "PNUT": {
        "description": "PNUT - Available on Kraken",
        "kraken_pair": "PNUTUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "POL": {
        "description": "POL - Available on Kraken",
        "kraken_pair": "POLUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "POPCAT": {
        "description": "POPCAT - Available on Kraken",
        "kraken_pair": "POPCATUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "PYTH": {
        "description": "PYTH - Available on Kraken",
        "kraken_pair": "PYTHUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "RENDER": {
        "description": "RENDER - Available on Kraken",
        "kraken_pair": "RENDERUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "REQ": {
        "description": "REQ - Available on Kraken",
        "kraken_pair": "REQUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "REZ": {
        "description": "REZ - Available on Kraken",
        "kraken_pair": "REZUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "RSR": {
        "description": "RSR - Available on Kraken",
        "kraken_pair": "RSRUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "RUNE": {
        "description": "RUNE - Available on Kraken",
        "kraken_pair": "RUNEUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "SAGA": {
        "description": "SAGA - Available on Kraken",
        "kraken_pair": "SAGAUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "SAND": {
        "description": "SAND - Available on Kraken",
        "kraken_pair": "SANDUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "SEI": {
        "description": "SEI - Available on Kraken",
        "kraken_pair": "SEIUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "SNX": {
        "description": "SNX - Available on Kraken",
        "kraken_pair": "SNXUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "SPX": {
        "description": "SPX - Available on Kraken",
        "kraken_pair": "SPXUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "STG": {
        "description": "STG - Available on Kraken",
        "kraken_pair": "STGUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "STRK": {
        "description": "STRK - Available on Kraken",
        "kraken_pair": "STRKUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "SUI": {
        "description": "SUI - Available on Kraken",
        "kraken_pair": "SUIUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "SUPER": {
        "description": "SUPER - Available on Kraken",
        "kraken_pair": "SUPERUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "SUSHI": {
        "description": "SUSHI - Available on Kraken",
        "kraken_pair": "SUSHIUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "TAO": {
        "description": "TAO - Available on Kraken",
        "kraken_pair": "TAOUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "TIA": {
        "description": "TIA - Available on Kraken",
        "kraken_pair": "TIAUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "TNSR": {
        "description": "TNSR - Available on Kraken",
        "kraken_pair": "TNSRUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "TON": {
        "description": "TON - Available on Kraken",
        "kraken_pair": "TONUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "TRUMP": {
        "description": "TRUMP - Available on Kraken",
        "kraken_pair": "TRUMPUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "TURBO": {
        "description": "TURBO - Available on Kraken",
        "kraken_pair": "TURBOUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "UNI": {
        "description": "UNI - Available on Kraken",
        "kraken_pair": "UNIUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "USUAL": {
        "description": "USUAL - Available on Kraken",
        "kraken_pair": "USUALUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "XLM": {
        "description": "XLM - Available on Kraken",
        "kraken_pair": "XXLMZUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "YGG": {
        "description": "YGG - Available on Kraken",
        "kraken_pair": "YGGUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "ZEREBRO": {
        "description": "ZEREBRO - Available on Kraken",
        "kraken_pair": "ZEREBROUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "ZETA": {
        "description": "ZETA - Available on Kraken",
        "kraken_pair": "ZETAUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "COMP": {
        "description": "COMP - Available on Kraken",
        "kraken_pair": "COMPUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "OP": {
        "description": "OP - Available on Kraken",
        "kraken_pair": "OPUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "UMA": {
        "description": "UMA - Available on Kraken",
        "kraken_pair": "UMAUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "W": {
        "description": "W - Available on Kraken",
        "kraken_pair": "WUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "SOL": {
        "description": "Solana - Available on Kraken",
        "kraken_pair": "SOLUSD",
        "hl_order_type": "limit",
        "price_precision": 4,
        "position_size": 12.0,
        "margin_size": 4.0
    },
    "DOGE": {
        "description": "Dogecoin - Available on Kraken",
        "kraken_pair": "XDGUSD",
        "hl_order_type": "limit",
        "price_precision": 6,
        "position_size": 12.0,
        "margin_size": 4.0
    }
}

# Define available trading pairs with their configuration

def get_available_pairs() -> Dict:
    """
    Get all available trading pairs
    
    Returns:
        Dictionary of available pairs with their configurations
    """
    return AVAILABLE_PAIRS

def get_available_pairs_list() -> List[str]:
    """
    Get list of available pairs symbols
    
    Returns:
        List of available pair symbols
    """
    return list(AVAILABLE_PAIRS.keys())

def format_pairs_description() -> str:
    """
    Format available pairs as readable text for Telegram
    
    Returns:
        Formatted string of available pairs with descriptions
    """
    formatted = "📊 *Available Trading Pairs*\n\n"
    
    for symbol, config in AVAILABLE_PAIRS.items():
        special_note = ""
        if symbol == "HYPE":
            special_note = " _(Special: both spot and perp on Hyperliquid)_"
            
        formatted += f"• *{symbol}*: {config['description']}{special_note}\n"
        
    formatted += "\nUse these symbols when selecting tokens for your trading bot."
    return formatted

def validate_pair_selection(pairs: List[str]) -> List[str]:
    """
    Validate a list of user-selected pairs
    
    Args:
        pairs: List of pair symbols selected by user
        
    Returns:
        List of valid pair symbols (invalid ones removed)
    """
    valid_pairs = []
    
    for pair in pairs:
        if pair in AVAILABLE_PAIRS:
            valid_pairs.append(pair)
        else:
            logger.warning(f"Invalid pair selected: {pair}")
            
    return valid_pairs

def check_hyperliquid_perpetuals() -> Set[str]:
    """
    Check which perpetuals are currently available on Hyperliquid
    
    Returns:
        Set of available perpetual symbols on Hyperliquid
    """
    try:
        # Use meta endpoint which is more reliable and doesn't require authentication
        response = requests.post("https://api.hyperliquid.xyz/info", json={"type": "meta"})
        
        if response.status_code == 200:
            data = response.json()
            if 'universe' in data:
                # Extract token names from universe list
                return {coin['name'] for coin in data['universe']}
            else:
                logger.error("No 'universe' field in Hyperliquid API response")
        else:
            logger.error(f"Failed to fetch Hyperliquid perpetuals: {response.status_code}")
            
    except Exception as e:
        logger.error(f"Error checking Hyperliquid perpetuals: {str(e)}")
        
    # Return all tokens in AVAILABLE_PAIRS as default if API call fails
    # This ensures all defined tokens are considered available
    return {k for k in AVAILABLE_PAIRS.keys() if k != "HYPE"}  # All tokens except HYPE (which is special case)

def check_kraken_spot_pairs() -> Set[str]:
    """
    Check which spot pairs are currently available on Kraken
    
    Returns:
        Set of available spot symbols on Kraken
    """
    try:
        response = requests.get("https://api.kraken.com/0/public/AssetPairs")
        
        if response.status_code == 200:
            data = response.json()
            
            if "result" in data:
                # Map Kraken's unusual asset naming to standard symbols
                kraken_to_standard = {
                    # Generate complete mapping from all AVAILABLE_PAIRS
                }
                
                # Automatically populate the mapping from AVAILABLE_PAIRS
                for symbol, config in AVAILABLE_PAIRS.items():
                    if config.get("kraken_pair") is not None:
                        kraken_to_standard[config["kraken_pair"]] = symbol
                
                available_pairs = set()
                for pair_name in data["result"].keys():
                    if pair_name in kraken_to_standard:
                        available_pairs.add(kraken_to_standard[pair_name])
                        
                return available_pairs
            else:
                logger.error("No 'result' field in Kraken API response")
                
        else:
            logger.error(f"Failed to fetch Kraken pairs: {response.status_code}")
            
    except Exception as e:
        logger.error(f"Error checking Kraken pairs: {str(e)}")
        
    # Return default list if API call fails - include all tokens that have kraken_pair defined
    return {symbol for symbol, config in AVAILABLE_PAIRS.items() if config.get("kraken_pair") is not None}

def get_active_trading_pairs() -> List[str]:
    """
    Get tokens available for trading
    
    Returns:
        List of available trading pairs
    """
    try:
        # Return ALL tokens in AVAILABLE_PAIRS
        # This makes all defined tokens available for selection
        return sorted(list(AVAILABLE_PAIRS.keys()))
    except Exception as e:
        logger.error(f"Error getting active trading pairs: {str(e)}")
        # Return all available pairs as fallback
        return sorted(list(AVAILABLE_PAIRS.keys()))
import os
from dotenv import load_dotenv

load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

investment = 100
SYMBOLS = [
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT"
]

TRANSACTION_COST = 0.002
GAIN_TARGET = 0.03

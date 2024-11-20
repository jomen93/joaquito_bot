import matplotlib.pyplot as plt

from app.services.binance_service import BinanceService
from app.config import BINANCE_API_KEY, BINANCE_SECRET_KEY, SYMBOLS
from app.services.logger_service import LoggerService

from IPython import embed


# Init the logger
logger = LoggerService()

binance_service = BinanceService(BINANCE_API_KEY, BINANCE_SECRET_KEY)
logger.log("INFO", "Binance Service")
connection_status = binance_service.test_connection()

if connection_status:
    print("Conecction stablished!")


for symbol in SYMBOLS: 
    print(symbol)
    df_symbol = binance_service.fetch_historical_data(symbol, interval="1h", start_date="2017-01-01")
    df_symbol.to_csv(symbol+".csv", index=False)

#


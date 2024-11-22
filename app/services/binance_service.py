import os
import time
import pandas as pd
from datetime import datetime, timedelta
from requests.exceptions import HTTPError

from binance.client import Client
from app.services.risk_analysis import RiskAnalysis
from app.services.logger_service import LoggerService
from app.config import (
    USE_TESTNET,
    TESTNET_API_KEY, 
    TESTNET_SECRET_KEY,
    BINANCE_API_KEY,
    BINANCE_SECRET_KEY)

from IPython import embed


class BinanceService:

    def __init__(self, api_key, secret_key, output_dir="crypto_data"):
        
        self.output_dir = output_dir
        self.logger = LoggerService()
        self.risk_analyzer = RiskAnalysis()

        if USE_TESTNET:
            self.logger.log("INFO", "Initializate Binance Client in TESTNET mode.")
            self.client = Client(TESTNET_API_KEY, TESTNET_SECRET_KEY)
            self.client.API_URL = "https://testnet.binance.vision/api"
        else:
            self.logger.log("INFO", "Initializating Binance Cliente in REAL MARKET mode.")
            self.client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)

    def _is_data_stale(self, symbol, interval="1h"):
        file_path = os.path.join(self.output_dir, f"{symbol}_{interval}.csv")
        if not os.path.exists(file_path):
            self.logger.log("INFO", f"No data file_found for {symbol}.")
            return True
        
        df = pd.read_csv(file_path)
        if df.empty:
            self.logger.log("INFO", f"Data file for {symbol} is empty.")
            return True

        last_record_time = pd.to_datetime(df["time"].iloc[-1])
        time_diference = datetime.utcnow() - last_record_time
        self.logger.log("INFO", f"Last record time for {symbol}: {last_record_time}")
        return time_diference > timedelta(hours=1)


    def fetch_historical_data(self, symbol, interval="1h", start_date="2017-01-01"):
        max_attemps = 5
        
        if not self._is_data_stale(symbol, interval):
            self.logger.log("INFO", f"Data for {symbol} is up-to-date.")
            return pd.read_csv(os.path.join(self.output_dir, f"{symbol}_{interval}.csv"))
        
        self.logger.log("INFO", f"Starting data fetch for {symbol} with interval {interval} from {start_date}.")

        all_data = []
        start_timestamp = int(pd.to_datetime(start_date).timestamp() * 1000)

        while True:
            try:
                klines = self.client.get_klines(
                    symbol=symbol,
                    interval=interval,
                    startTime=start_timestamp,
                    limit=1000
                )

                if not klines:
                    self.logger.log("INFO", f"No more data available for {symbol}.")
                    break

                for kline in klines:
                    all_data.append({
                        "time": pd.to_datetime(kline[0], unit="ms"),  # Timestamp en milisegundos
                        "open": float(kline[1]),
                        "high": float(kline[2]),
                        "low": float(kline[3]),
                        "close": float(kline[4]),
                        "volume": float(kline[5])
                    })

                start_timestamp = klines[-1][0] + 1
                self.logger.log("INFO", f"Fetched {len(klines)} row, total: {len(all_data)} rows so far.")
                time.sleep(0.2)
            except HTTPError as http_err:
                self.logger.log("ERROR", f"HTTP error ocurred: {http_err}")
                break

            except Exception as e:
                self.logger.log("ERROR", f"Error ocurred: {e}")
                max_attemps -= 1
                if max_attemps == 0:
                    self.logger.log("ERROR", "Max retries reached. Exiting...")
                    break
                time.sleep(1)

        df = pd.DataFrame(all_data)
        df.to_csv(os.path.join(self.output_dir, f"{symbol}_{interval}.csv"), index=False)
        self.logger.log("INFO", f"Data saved for {symbol}. Total rows: {len(df)}")
        return df

    def create_order(self, symbol: str, order_type: str, quantity: float, price=None):
        """
        Create a order Buy/Sell based on the investment environment 

        Args:
        -----
            symbol (str): Cryptocurrency pair
            side (str): buy or sell
            order_type (str): Order type "Market" or "Limit"
            quantity (float): Quantity to buy/sell
            price (float, Optional); Price (Required for limit orders)

        Returns:
        --------
            dict: API response (or simulated in the case of Testnet)
        """
        try:
            if order_type == Client.ORDER_TYPE_LIMIT:
                if not price:
                    raise ValueError("Price is required for LIMIT orders.")
                order = self.client.create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    quantity=quantity,
                    price=price
                )

            elif order_type == Client.ORDER_TYPE_MARKET:
                order = self.client.create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    quantity=quantity
                )
            else:
                raise ValueError("Invalid order type specified")

            self.logger.log("INFO", f"Order created successfully: {order}")
            return order

        except Exception as e:
            self.logger.log("ERROR", f"Failed to create order: {e}")
            return None



    def test_connection(self):

        try:
            status = self.client.ping()
            if status == {}:
                return True
            else:
                return False
        except Exception as e:
            return f"Error: {e}"

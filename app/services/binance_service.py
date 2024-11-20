import os
import time

from binance.client import Client
from requests.exceptions import HTTPError

import pandas as pd
from app.services.logger_service import LoggerService

from IPython import embed


class BinanceService:

    def __init__(self, api_key, secret_key, output_dir="crypto_data"):
        self.client = Client(api_key, secret_key)
        self.output_dir = output_dir
        self.logger = LoggerService()


    def fetch_historical_data(self, symbol, interval="1h", start_date="2017-01-01"):
        all_data = []
        start_timestamp = int(pd.to_datetime(start_date).timestamp() * 1000)
        max_attemps = 5

        self.logger.log("INFO", f"Starting data fetch for {symbol} with interval {interval} from {start_date}.")

    
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
        return df

    def test_connection(self):

        try:
            status = self.client.ping()
            if status == {}:
                return True
            else:
                return False
        except Exception as e:
            return f"Error: {e}"

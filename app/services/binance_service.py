import pandas as pd

from binance.client import Client


class BinanceService:

    def __init__(self, api_key, secret_key):
        self.client = Client(api_key, secret_key)

    def fetch_historical_data(self, symbol:str, interval: str = "1h", limit: int = 90):
        klines = self.client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit
        )
        
        data = {
            "time": [int(k[0]) for k in klines],
            "open": [float(k[1]) for k in klines],
            "high": [float(k[2]) for k in klines],
            "low": [float(k[3]) for k in klines],
            "close": [float(k[4]) for k in klines],
            "volume": [float(k[5]) for k in klines]
        }
        
        df = pd.DataFrame(data)

        # Convert the time
        df["time"] = pd.to_datetime(df["time"], unit="ms")

        # Technical indicators
        df["SMA_14"] = df["close"].rolling(window=14).mean()  # SMA de 14 períodos
        df["EMA_14"] = df["close"].ewm(span=14, adjust=False).mean()  # EMA de 14 períodos
    
        # RSI
        delta = df["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df["RSI_14"] = 100 - (100 / (1 + rs))

        # Bollinger Bands
        df["BB_MID"] = df["close"].rolling(window=20).mean()  # SMA de 20 períodos
        df["BB_UPPER"] = df["BB_MID"] + 2 * df["close"].rolling(window=20).std()
        df["BB_LOWER"] = df["BB_MID"] - 2 * df["close"].rolling(window=20).std()
        
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

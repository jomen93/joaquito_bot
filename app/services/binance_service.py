from binance.client import Client


class BinanceService:

    def __init__(self, api_key, secret_key):
        self.client = Client(api_key, secret_key)

    def test_connection(self):

        try:
            status = self.client.ping()
            if status == {}:
                return True
            else:
                return False
        except Exception as e:
            return f"Error: {e}"

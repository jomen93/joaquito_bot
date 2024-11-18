from app.services.binance_service import BinanceService
from app.config import BINANCE_API_KEY, BINANCE_SECRET_KEY


binance_service = BinanceService(BINANCE_API_KEY, BINANCE_SECRET_KEY)
connection_status = binance_service.test_connection()
print(connection_status)



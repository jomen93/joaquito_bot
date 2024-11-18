import matplotlib.pyplot as plt

from app.services.binance_service import BinanceService
from app.config import BINANCE_API_KEY, BINANCE_SECRET_KEY, SYMBOLS
from IPython import embed

binance_service = BinanceService(BINANCE_API_KEY, BINANCE_SECRET_KEY)
connection_status = binance_service.test_connection()

if connection_status:
    print("Conecction stablished!")


for symbol in SYMBOLS: 
    print(symbol)
    df_symbol = binance_service.fetch_historical_data(symbol, interval="1h", start_date="2017-01-01")
    df_symbol.to_csv(symbol+".csv", index=False)

#
# plt.figure(figsize=(12, 6))
# plt.plot(df['time'], df['open'], label='Open', linewidth=1.5)
# plt.plot(df['time'], df['high'], label='High', linewidth=1.5)
# plt.plot(df['time'], df['low'], label='Low', linewidth=1.5)
# plt.plot(df['time'], df['close'], label='Close', linewidth=1.5)
#
# # Configurando etiquetas y título
# plt.title('Comportamiento del Precio de la Criptomoneda', fontsize=14)
# plt.xlabel('Time', fontsize=12)
# plt.ylabel('Price', fontsize=12)
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
#
# # Mostrar la gráfica
# plt.show()
#


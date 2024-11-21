from app.services.risk_analysis import RiskAnalysis
from app.services.logger_service import LoggerService
from app.services.binance_service import BinanceService
from app.config import BINANCE_API_KEY, BINANCE_SECRET_KEY, SYMBOLS

from IPython import embed

# Init the logger
logger = LoggerService()
logger.set_context(session="Joaco_001")

# Init the service
binance_service = BinanceService(BINANCE_API_KEY, BINANCE_SECRET_KEY)
logger.log("INFO", "Initialize the Binance Service")

# Init risk service
risk_analysis = RiskAnalysis()
logger.log("INFO", "Risk Analysis model initialized.")

# Test connection
connection_status = binance_service.test_connection()
if connection_status:
    logger.log("INFO", "Conecction stablished !")
else:
    logger.log("ERROR", "Conecction failed !")


# Download the data
for symbol in SYMBOLS:
    logger.log("INFO", f"Processing symbol: {symbol}")

    # Fetch historical data
    df_symbol = binance_service.fetch_historical_data(
        symbol, 
        interval="1h", 
        start_date="2017-01-01")
    if df_symbol.empty:
        logger.log("WARNING", f"No data available for symbol {symbol}. Skipping !")

    # Analyze risk
    risk_level = risk_analysis.assess_risk(df_symbol)
    logger.log("INFO", f"risk level for {symbol}: {risk_level}")

    if risk_level == "L":
        logger.log("INFO", f"Low risk detected for {symbol}. Procceding with investment !")
    elif risk_level == "M":
        logger.log("WARNING", f"Medium risk detected for symbol {symbol}. Consider additional analysis.")

    else:
        logger.log("ERROR", f"High risk detected for {symbol}: Sikkiping investment")

logger.log("INFO", "Process completed!")


       

    






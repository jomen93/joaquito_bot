import pandas as pd


class RiskAnalysis:
    """
    Class to perform risk analysis based in historical data
    """

    def __init__(self):

        self.volatility_threshold = 0.05
        self.volume_threshold = 1000


    def _calculate_volatility(self, df):
        """
        Price volatility calculations
        """
        df["volatility"] = (df["high"] - df["low"]) / df["close"]

        return df["volatility"].mean()

    def _calculate_average_volumne(self, df):

        return df["volume"].mean()

    def assess_risk(self, df):
        
        volatility = self._calculate_volatility(df)
        avg_volume = self._calculate_average_volumne(df)

        volatility_condition = volatility > self.volatility_threshold
        volume_condition = avg_volume < self.volume_threshold

        if volatility_condition and volume_condition:
            return "H"
        elif volatility_condition or volume_condition:
            return "M"
        else:
            return "L"




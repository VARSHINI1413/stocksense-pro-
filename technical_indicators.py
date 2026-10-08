import numpy as np
import pandas as pd


class TechnicalIndicators:

    @staticmethod
    def calculate_rsi(series, period=14):

        delta = series.diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.ewm(
            alpha=1 / period,
            min_periods=period,
            adjust=False
        ).mean()

        avg_loss = loss.ewm(
            alpha=1 / period,
            min_periods=period,
            adjust=False
        ).mean()

        rs = avg_gain / avg_loss

        rsi = 100 - (100 / (1 + rs))

        return rsi

    @staticmethod
    def add_indicators(data):

        df = data.copy()

        # Moving averages
        df["SMA_7"] = df["Close"].rolling(7).mean()
        df["SMA_20"] = df["Close"].rolling(20).mean()
        df["SMA_50"] = df["Close"].rolling(50).mean()

        # RSI
        df["RSI"] = TechnicalIndicators.calculate_rsi(
            df["Close"],
            14
        )

        # Daily return
        df["Daily_Return"] = df["Close"].pct_change()

        # Annualized volatility
        df["Volatility_20"] = (
            df["Daily_Return"]
            .rolling(20)
            .std()
            * np.sqrt(252)
        )

        # Volume indicators
        df["Volume_SMA"] = (
            df["Volume"]
            .rolling(20)
            .mean()
        )

        df["Volume_Ratio"] = (
            df["Volume"] /
            df["Volume_SMA"]
        )

        df.dropna(inplace=True)

        return df

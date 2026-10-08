from data_fetcher import DataFetcher
from technical_indicators import TechnicalIndicators
from xgboost_model import XGBoostModel


class AnalysisEngine:

    def __init__(self, ticker):

        self.ticker = ticker

        self.fetcher = DataFetcher(ticker)

        self.model = XGBoostModel()

    def run_analysis(self):

        # 1. Fetch historical data
        data = self.fetcher.fetch_data()

        # 2. Add technical indicators
        data = TechnicalIndicators.add_indicators(
            data
        )

        # 3. Train model
        metrics = self.model.train(data)

        # 4. Predict next-day price
        predicted_price = (
            self.model.predict_next_day(data)
        )

        current_price = float(
            data["Close"].iloc[-1]
        )

        predicted_change = (
            (predicted_price - current_price)
            / current_price
        ) * 100

        # 5. ML signal
        if predicted_change > 1:
            ml_signal = "BUY"

        elif predicted_change < -1:
            ml_signal = "SELL"

        else:
            ml_signal = "HOLD"

        # 6. Technical signal
        rsi = float(data["RSI"].iloc[-1])

        if rsi < 35:
            technical_signal = "BUY"

        elif rsi > 65:
            technical_signal = "SELL"

        else:
            technical_signal = "HOLD"

        return {
            "data": data,
            "current_price": current_price,
            "predicted_price": predicted_price,
            "predicted_change": predicted_change,
            "rsi": rsi,
            "ml_signal": ml_signal,
            "technical_signal": technical_signal,
            "metrics": metrics
        }

import yfinance as yf
import pandas as pd


class DataFetcher:

    def __init__(self, ticker):
        self.ticker = ticker

    def fetch_data(self):
        try:
            data = yf.download(
                self.ticker,
                period="2y",
                auto_adjust=True,
                progress=False
            )

            if data.empty:
                raise ValueError("No data found for this ticker.")

            # Handle MultiIndex columns from yFinance
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)

            data.dropna(inplace=True)

            if len(data) < 100:
                raise ValueError(
                    "Insufficient historical data for analysis."
                )

            return data

        except Exception as e:
            raise RuntimeError(
                f"Unable to fetch stock data: {str(e)}"
            )

class PositionAnalyzer:

    def __init__(
        self,
        shares,
        purchase_price,
        current_price
    ):
        self.shares = shares
        self.purchase_price = purchase_price
        self.current_price = current_price

    def analyze_position(self):

        invested_capital = (
            self.shares *
            self.purchase_price
        )

        current_value = (
            self.shares *
            self.current_price
        )

        profit_loss = (
            current_value -
            invested_capital
        )

        profit_loss_percent = (
            profit_loss /
            invested_capital
        ) * 100

        return {
            "Invested Capital": invested_capital,
            "Current Market Value": current_value,
            "Profit/Loss": profit_loss,
            "Profit/Loss %": profit_loss_percent,
            "Break-even Price": self.purchase_price
        }


class PortfolioAdvisor:

    @staticmethod
    def get_recommendation(
        rsi,
        ml_signal,
        technical_signal,
        profit_loss_percent
    ):

        # More than 30% profit + technical SELL
        if (
            profit_loss_percent > 30
            and technical_signal == "SELL"
        ):
            return "SELL_ALL"

        # More than 20% profit + ML SELL
        if (
            profit_loss_percent > 20
            and ml_signal == "SELL"
        ):
            return "PARTIAL_SELL"

        # Less than 10% loss + technical BUY
        if (
            profit_loss_percent > -10
            and technical_signal == "BUY"
        ):
            return "AVERAGE_DOWN"

        # High RSI
        if rsi > 70:
            return "TAKE_PROFITS"

        # Strong BUY signals
        if (
            ml_signal == "BUY"
            and technical_signal == "BUY"
        ):
            return "BUY_MORE"

        return "HOLD"

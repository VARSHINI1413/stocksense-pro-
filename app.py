import streamlit as st
import matplotlib.pyplot as plt

from analysis_engine import AnalysisEngine
from portfolio_advisor import (
    PositionAnalyzer,
    PortfolioAdvisor
)


st.set_page_config(
    page_title="StockSense Pro",
    page_icon="📈",
    layout="wide"
)


st.title("📈 StockSense Pro")
st.subheader(
    "AI-Powered Stock Analysis & Portfolio Advisor"
)


ticker = st.text_input(
    "Enter Stock Ticker",
    value="RELIANCE.NS"
).upper()


if st.button("Analyze Stock"):

    with st.spinner("Analyzing stock..."):

        try:

            engine = AnalysisEngine(ticker)

            result = engine.run_analysis()

            data = result["data"]

            current_price = result[
                "current_price"
            ]

            predicted_price = result[
                "predicted_price"
            ]

            predicted_change = result[
                "predicted_change"
            ]

            rsi = result["rsi"]

            # Price section
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Current Price",
                    f"{current_price:.2f}"
                )

            with col2:
                st.metric(
                    "Predicted Next-Day Price",
                    f"{predicted_price:.2f}"
                )

            with col3:
                st.metric(
                    "Expected Change",
                    f"{predicted_change:.2f}%"
                )

            # Chart
            st.subheader(
                "Price & Moving Averages"
            )

            chart_data = data.tail(90)

            fig, ax = plt.subplots(
                figsize=(12, 5)
            )

            ax.plot(
                chart_data.index,
                chart_data["Close"],
                label="Close"
            )

            ax.plot(
                chart_data.index,
                chart_data["SMA_20"],
                label="SMA 20"
            )

            ax.plot(
                chart_data.index,
                chart_data["SMA_50"],
                label="SMA 50"
            )

            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            ax.legend()

            st.pyplot(fig)

            # Signals
            st.subheader("Trading Signals")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "RSI",
                    f"{rsi:.2f}"
                )

            with col2:
                st.metric(
                    "ML Signal",
                    result["ml_signal"]
                )

            with col3:
                st.metric(
                    "Technical Signal",
                    result["technical_signal"]
                )

            # Model metrics
            st.subheader("Model Performance")

            metrics = result["metrics"]

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "R² Score",
                    f"{metrics['R2 Score']:.3f}"
                )

            with col2:
                st.metric(
                    "RMSE",
                    f"{metrics['RMSE']:.2f}"
                )

            with col3:
                st.metric(
                    "MAE",
                    f"{metrics['MAE']:.2f}"
                )

            with col4:
                st.metric(
                    "Directional Accuracy",
                    f"{metrics['Directional Accuracy']:.2f}%"
                )

            # Portfolio section
            st.subheader(
                "Portfolio Advisor"
            )

            shares = st.number_input(
                "Shares Owned",
                min_value=0.0,
                value=0.0
            )

            purchase_price = st.number_input(
                "Purchase Price",
                min_value=0.0,
                value=0.0
            )

            if shares > 0 and purchase_price > 0:

                position = PositionAnalyzer(
                    shares,
                    purchase_price,
                    current_price
                )

                position_data = (
                    position.analyze_position()
                )

                recommendation = (
                    PortfolioAdvisor
                    .get_recommendation(
                        rsi,
                        result["ml_signal"],
                        result["technical_signal"],
                        position_data["Profit/Loss %"]
                    )
                )

                st.write(
                    "### Recommendation"
                )

                st.success(
                    recommendation
                )

                st.write(
                    f"Invested Capital: "
                    f"{position_data['Invested Capital']:.2f}"
                )

                st.write(
                    f"Current Market Value: "
                    f"{position_data['Current Market Value']:.2f}"
                )

                st.write(
                    f"Profit/Loss: "
                    f"{position_data['Profit/Loss']:.2f}"
                )

                st.write(
                    f"Profit/Loss %: "
                    f"{position_data['Profit/Loss %']:.2f}%"
                )

        except Exception as e:

            st.error(
                f"Analysis failed: {str(e)}"
            )

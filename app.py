
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


# Stock selection dropdown
stock_options = {
    "Reliance Industries": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Tata Motors": "TMPV.NS",
    "ITC": "ITC.NS",
    "Wipro": "WIPRO.NS",
    "State Bank of India": "SBIN.NS",
    "Larsen & Toubro": "LT.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Amazon": "AMZN",
    "Alphabet (Google)": "GOOGL",
    "Tesla": "TSLA",
    "Meta Platforms": "META"
}


col1, col2 = st.columns([3, 1])

with col1:
    selected_stock = st.selectbox(
        "Choose a stock to analyze",
        options=list(stock_options.keys())
    )

with col2:
    st.write("")
    st.write("")
    analyze_button = st.button(
        "Analyze Stock",
        type="primary",
        use_container_width=True
    )


ticker = stock_options[selected_stock]


if analyze_button:

    with st.spinner(f"Analyzing {selected_stock}..."):

        try:
            engine = AnalysisEngine(ticker)
            result = engine.run_analysis()

            data = result["data"]

            current_price = result["current_price"]
            predicted_price = result["predicted_price"]
            predicted_change = result["predicted_change"]
            rsi = result["rsi"]

            # Stock overview
            st.header(f"{selected_stock} ({ticker})")

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

            # Price chart
            st.subheader("Price & Moving Averages")

            chart_data = data.tail(90)

            fig, ax = plt.subplots(figsize=(12, 5))

            ax.plot(
                chart_data.index,
                chart_data["Close"],
                label="Close Price"
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
            ax.set_title(f"{selected_stock} Price Trend")
            ax.legend()
            ax.grid(alpha=0.25)

            st.pyplot(fig)
            plt.close(fig)

            # Trading signals
            st.subheader("Trading Signals")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("RSI", f"{rsi:.2f}")

            with col2:
                st.metric(
                    "ML Signal",
                    str(result["ml_signal"])
                )

            with col3:
                st.metric(
                    "Technical Signal",
                    str(result["technical_signal"])
                )

            # Model performance
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

            # Portfolio advisor
            st.subheader("Portfolio Advisor")

            st.write(
                "Enter your holdings to review your position."
            )

            col1, col2 = st.columns(2)

            with col1:
                shares = st.number_input(
                    "Shares Owned",
                    min_value=0.0,
                    value=0.0,
                    step=1.0
                )

            with col2:
                purchase_price = st.number_input(
                    "Purchase Price per Share",
                    min_value=0.0,
                    value=0.0,
                    step=1.0
                )

            if shares > 0 and purchase_price > 0:

                position = PositionAnalyzer(
                    shares,
                    purchase_price,
                    current_price
                )

                position_data = position.analyze_position()

                recommendation = PortfolioAdvisor.get_recommendation(
                    rsi,
                    result["ml_signal"],
                    result["technical_signal"],
                    position_data["Profit/Loss %"]
                )

                st.subheader("Position Summary")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Invested Capital",
                        f"{position_data['Invested Capital']:.2f}"
                    )

                with col2:
                    st.metric(
                        "Current Market Value",
                        f"{position_data['Current Market Value']:.2f}"
                    )

                with col3:
                    profit_loss = position_data["Profit/Loss"]

                    st.metric(
                        "Profit / Loss",
                        f"{profit_loss:.2f}",
                        delta=f"{position_data['Profit/Loss %']:.2f}%"
                    )

                st.subheader("Portfolio Recommendation")

                st.info(str(recommendation))

            else:
                st.caption(
                    "Enter shares owned and purchase price to "
                    "calculate your portfolio position."
                )

            st.caption(
                "Disclaimer: Stock predictions are estimates, "
                "not guarantees. This tool is for educational "
                "purposes and is not financial advice."
            )

        except Exception as e:
            st.error(f"Analysis failed: {e}")
            st.info(
                "Check your internet connection, stock ticker "
                "availability, and project dependencies. "
                "If the error persists, review the terminal traceback."
            )


import streamlit as st
import matplotlib.pyplot as plt

from analysis_engine import AnalysisEngine
from portfolio_advisor import (
    PositionAnalyzer,
    PortfolioAdvisor
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="StockSense Pro",
    page_icon="📈",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM UI STYLING
# --------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(
            135deg,
            #f5f8ff 0%,
            #f8fbff 55%,
            #effaf5 100%
        );
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1250px;
    }

    h1 {
        color: #16325c;
        font-weight: 800;
        letter-spacing: -1px;
    }

    h2, h3 {
        color: #24446d;
        font-weight: 700;
    }

    .stButton > button {
        background: linear-gradient(
            90deg,
            #2563eb,
            #0f9f86
        );
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.65rem 1rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 14px rgba(37, 99, 235, 0.22);
        color: white;
        border: none;
    }

    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.92);
        border: 1px solid #dce7f7;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0 3px 12px rgba(30, 64, 120, 0.05);
        transition: transform 0.2s ease,
                    box-shadow 0.2s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 7px 18px rgba(30, 64, 120, 0.10);
    }

    [data-testid="stMetricLabel"] {
        color: #5b7190;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #16325c;
        font-weight: 750;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        border-radius: 9px;
        border-color: #d6e2f2;
        background-color: white;
    }

    [data-testid="stPlotlyChart"],
    [data-testid="stPyplot"] {
        background: white;
        border: 1px solid #e0e9f7;
        border-radius: 14px;
        padding: 10px;
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    hr {
        border-color: #e0e9f5;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div style="
    background: linear-gradient(120deg, #e7efff, #e7f9f1);
    padding: 25px;
    border-radius: 16px;
    border: 1px solid #dce8f7;
    margin-bottom: 22px;
">
    <h1 style="margin:0; color:#16325c;">
        📈 StockSense
        <span style="color:#0f9f86;">Pro</span>
    </h1>
    <p style="margin:8px 0 0 0; color:#536b8c; font-size:16px;">
        AI-Powered Stock Analysis &amp; Portfolio Advisor
    </p>
    <p style="margin:5px 0 0 0; color:#71839b; font-size:13px;">
        Smarter insights. Better-informed decisions.
    </p>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# STOCK SELECTION
# --------------------------------------------------

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

st.subheader("🔎 Select a Stock")

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
        "📊 Analyze Stock",
        type="primary",
        use_container_width=True
    )

ticker = stock_options[selected_stock]


# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

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
            metrics = result["metrics"]

            if data is None or data.empty:
                st.error("No stock data was returned.")
                st.stop()

            # ------------------------------------------
            # STOCK OVERVIEW
            # ------------------------------------------

            st.divider()

            st.subheader(
                f"📈 {selected_stock} ({ticker})"
            )

            st.caption(
                "Review historical prices, model estimates, "
                "technical indicators and your portfolio position."
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Current Price",
                    f"{current_price:,.2f}"
                )

            with col2:
                st.metric(
                    "Predicted Next-Day Price",
                    f"{predicted_price:,.2f}"
                )

            with col3:
                st.metric(
                    "Expected Change",
                    f"{predicted_change:+.2f}%"
                )

            # ------------------------------------------
            # PRICE CHART
            # ------------------------------------------

            st.divider()
            st.subheader("📉 Price & Moving Averages")

            chart_data = data.tail(90)

            fig, ax = plt.subplots(figsize=(12, 5))

            fig.patch.set_facecolor("white")
            ax.set_facecolor("#fbfdff")

            ax.plot(
                chart_data.index,
                chart_data["Close"],
                label="Close Price",
                color="#2563eb",
                linewidth=2
            )

            if "SMA_20" in chart_data.columns:
                ax.plot(
                    chart_data.index,
                    chart_data["SMA_20"],
                    label="SMA 20",
                    color="#f59e0b",
                    linewidth=1.8
                )

            if "SMA_50" in chart_data.columns:
                ax.plot(
                    chart_data.index,
                    chart_data["SMA_50"],
                    label="SMA 50",
                    color="#0f9f86",
                    linewidth=1.8
                )

            ax.set_xlabel("Date", color="#64748b")
            ax.set_ylabel("Price", color="#64748b")

            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_color("#dce5f0")
            ax.spines["bottom"].set_color("#dce5f0")

            ax.grid(
                True,
                linestyle="--",
                alpha=0.25
            )

            ax.tick_params(colors="#64748b")

            ax.set_title(
                f"{selected_stock} - Price Trend",
                fontsize=14,
                fontweight="bold",
                color="#16325c",
                pad=15
            )

            ax.legend(
                frameon=False,
                loc="upper left"
            )

            fig.tight_layout()

            st.pyplot(fig)
            plt.close(fig)

            # ------------------------------------------
            # TRADING SIGNALS
            # ------------------------------------------

            st.divider()
            st.subheader("🎯 Trading Signals")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Relative Strength Index (RSI)",
                    f"{rsi:.2f}"
                )

            with col2:
                st.markdown("**ML Signal**")
                st.info(str(result["ml_signal"]))

            with col3:
                st.markdown("**Technical Signal**")
                st.info(str(result["technical_signal"]))

            st.caption(
                "Signals are model outputs and technical indicators, "
                "not guaranteed buy or sell recommendations."
            )

            # ------------------------------------------
            # MODEL PERFORMANCE
            # ------------------------------------------

            st.divider()
            st.subheader("🧠 Model Performance")

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

            with st.expander("ℹ️ Understand these metrics"):
                st.markdown("""
                - **R² Score:** Indicates how well the model explains
                  price variation. A higher score is generally better.
                - **RMSE:** Measures prediction errors and penalizes
                  larger errors more heavily.
                - **MAE:** Shows the average absolute prediction error.
                - **Directional Accuracy:** Measures how often the model
                  correctly predicts the direction of price movement.

                These values depend on the evaluation method and test data.
                They do not guarantee future performance.
                """)

            # ------------------------------------------
            # PORTFOLIO ADVISOR
            # ------------------------------------------

            st.divider()
            st.subheader("💼 Portfolio Advisor")

            st.write(
                "Enter your holdings to calculate your current position."
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

                st.markdown("#### Your Position")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Invested Capital",
                        f"{position_data['Invested Capital']:,.2f}"
                    )

                with col2:
                    st.metric(
                        "Current Market Value",
                        f"{position_data['Current Market Value']:,.2f}"
                    )

                with col3:
                    st.metric(
                        "Profit / Loss",
                        f"{position_data['Profit/Loss']:+,.2f}",
                        delta=(
                            f"{position_data['Profit/Loss %']:+.2f}%"
                        )
                    )

                st.markdown("#### Analysis Summary")

                st.info(str(recommendation))

            else:
                st.caption(
                    "Enter both shares owned and purchase price "
                    "to calculate your portfolio position."
                )

            # ------------------------------------------
            # DISCLAIMER
            # ------------------------------------------

            st.divider()

            st.caption(
                "⚠️ Disclaimer: Stock predictions are estimates, "
                "not guarantees. This dashboard is for educational "
                "and informational purposes only and is not financial advice."
            )

        except Exception as e:
            st.error(f"Analysis failed: {e}")

            with st.expander("Troubleshooting"):
                st.write(
                    "Check your internet connection, ticker symbol, "
                    "data availability, installed dependencies, and "
                    "the terminal traceback."
                )

else:
    # ----------------------------------------------
    # INITIAL SCREEN
    # ----------------------------------------------

    st.markdown("""
    <div style="
        background: rgba(255,255,255,0.85);
        padding: 28px;
        border: 1px solid #dce7f7;
        border-radius: 16px;
        text-align: center;
        margin-top: 15px;
    ">
        <div style="font-size:44px;">📊</div>
        <h3 style="color:#16325c;">Your Stock Analysis Dashboard</h3>
        <p style="color:#64748b;">
            Select a company above and click
            <b>Analyze Stock</b> to explore its price trends,
            prediction estimates, technical indicators and portfolio position.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📈 Price Trends")
        st.caption(
            "Explore closing prices and moving averages."
        )

    with col2:
        st.markdown("### 🧠 ML Insights")
        st.caption(
            "Review model predictions and evaluation metrics."
        )

    with col3:
        st.markdown("### 💼 Portfolio")
        st.caption(
            "Calculate the profit or loss on your holdings."
        )

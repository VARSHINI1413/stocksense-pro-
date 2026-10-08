# 📈 StockSense Pro

**AI-Powered Stock Prediction & Portfolio Analysis Platform**

StockSense Pro is an interactive stock analysis platform built with **Python and Streamlit**. It uses historical market data, technical indicators, and an **XGBoost regression model** to predict the next trading day's closing price and support data-informed investment decisions.

## 🚀 Features

* 📊 Historical stock data analysis using Yahoo Finance
* 📈 Technical indicators including RSI and Moving Averages
* 🤖 XGBoost-based next-day price prediction
* 📏 Model evaluation using R², RMSE, MAE, and Directional Accuracy
* 💼 Portfolio analysis and recommendation system
* 📉 Interactive stock charts
* 🖥️ Streamlit-based web interface

## 🛠️ Tech Stack

* **Python**
* **Streamlit**
* **XGBoost**
* **Pandas**
* **NumPy**
* **Scikit-learn**
* **yFinance**
* **Matplotlib**

## 📂 Project Structure

```text
StockSense-Pro/
│
├── app.py
├── analysis_engine.py
├── data_fetcher.py
├── technical_indicators.py
├── xgboost_model.py
├── portfolio_advisor.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/stocksense-pro.git
cd stocksense-pro
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will open locally at:

```text
http://localhost:8501
```

## 📊 How It Works

```text
Stock Ticker
     ↓
Yahoo Finance Data
     ↓
Feature Engineering
     ↓
Technical Indicators
     ↓
XGBoost Model
     ↓
Next-Day Price Prediction
     ↓
Trading Signals
     ↓
Portfolio Advisor
```

## 🎯 Project Goal

The goal of StockSense Pro is to combine **data analysis, machine learning, and financial indicators** into an accessible platform that helps users explore stock trends and make more informed decisions.

## ⚠️ Disclaimer

StockSense Pro is an academic and educational project. Predictions and recommendations are generated for analysis purposes and should not be considered professional financial advice.

## 👩‍💻 Author

**M. Varshini**
B.Sc. Computer Science
D.G. Vaishnav College



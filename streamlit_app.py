import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Define presidents and their inauguration dates
presidents = {
    "Joe Biden (2021)": datetime(2021, 1, 20),
    "Donald Trump (2017)": datetime(2017, 1, 20),
    "Donald Trump (2025)": datetime(2025, 1, 20),
    "Barack Obama (2009)": datetime(2009, 1, 20),
    "George W. Bush (2001)": datetime(2001, 1, 20),
    "Bill Clinton (1993)": datetime(1993, 1, 20),
    "George H. W. Bush (1989)": datetime(1989, 1, 20),
    "Ronald Reagan (1981)": datetime(1981, 1, 20),
    "Jimmy Carter (1977)": datetime(1977, 1, 20),
    "Gerald Ford (1974)": datetime(1974, 8, 9),
    "Richard Nixon (1969)": datetime(1969, 1, 20),
    "Lyndon B. Johnson (1963)": datetime(1963, 11, 22),
    "John F. Kennedy (1961)": datetime(1961, 1, 20)
}

st.title("S&P 500 Performance by Presidential Term")

# User selects presidents to compare
selected_presidents = st.multiselect(
    "Select presidents to compare:",
    options=list(presidents.keys()),
    default=["Joe Biden (2021)", "Donald Trump (2025)", "Donald Trump (2017)"]
)

# How many days into term to display?
max_days = int(365.25*4)

# Download S&P 500 data
@st.cache_data

def get_sp500_data():
    return yf.download("^GSPC", start="1961-01-01", auto_adjust=True)["Close"]

sp500 = get_sp500_data()

# Prepare data
plt.figure(figsize=(10, 6))
all_series = {}
for pres in selected_presidents:
    start = presidents[pres]
    end = start + timedelta(days=max_days)
    data = sp500.loc[(sp500.index >= start) & (sp500.index <= end)].copy()
    data = data[:max_days]  # ensure alignment if weekends/holidays
    data = data.reset_index()
    data["Day"] = (data["Date"] - start).dt.days
    data["% Change"] = data["^GSPC"] / data["^GSPC"].iloc[0] * 100 - 100
    all_series[pres] = data

if len(all_series):
    min_days = min(len(data) for data in all_series.values())
    days = min(int(min_days*1.10), max_days)

    for pres, data in all_series.items():
        data = data[:days]
        plt.plot(data["Day"], data["% Change"], label=pres)

plt.axhline(0, color='gray', linestyle='--')
plt.xlabel("Days into Term")
plt.ylabel("% Change in S&P 500")
plt.title("S&P 500 Performance During Presidential Terms")
plt.legend()
plt.grid(True)
st.pyplot(plt)

st.caption("Data sourced from Yahoo Finance using yfinance.")
st.caption("Streamlit App developed with ChatGPT 4o assistance.")

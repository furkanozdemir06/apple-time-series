import datetime
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="AAPL Stock Analysis", layout="wide")
st.title("🍎 Apple (AAPL) Time Series Analysis")

# Sidebar
days_back = st.sidebar.slider("Historical Data Range (Days)", 180, 1095, 720)
ma_short = st.sidebar.slider("Short Moving Average (Days)", 5, 50, 20)
ma_long = st.sidebar.slider("Long Moving Average (Days)", 20, 200, 50)

# Download Data
@st.cache_data
def get_data(days):
    end = datetime.date.today()
    start = end - datetime.timedelta(days=days)
    df = yf.download('AAPL', start=start, end=end, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df

df = get_data(days_back)

# Calculate Moving Averages
df['MA_Short'] = df['Close'].rolling(window=ma_short).mean()
df['MA_Long'] = df['Close'].rolling(window=ma_long).mean()

# Key Metrics
last_price = float(df['Close'].iloc[-1])
change = last_price - float(df['Close'].iloc[-2])

c1, c2, c3 = st.columns(3)
c1.metric("Latest Close", f"${last_price:.2f}", f"{change:+.2f}$")
c2.metric("Short MA", f"${df['MA_Short'].iloc[-1]:.2f}")
c3.metric("Long MA", f"${df['MA_Long'].iloc[-1]:.2f}")

# Price & Moving Average Chart
st.subheader("📊 Price Action & Moving Averages")
fig = go.Figure()

# Close Price Line
fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name="Close Price", line=dict(color="blue")))

# Moving Averages
fig.add_trace(go.Scatter(x=df.index, y=df['MA_Short'], name=f"{ma_short}-Day MA", line=dict(color="orange")))
fig.add_trace(go.Scatter(x=df.index, y=df['MA_Long'], name=f"{ma_long}-Day MA", line=dict(color="green")))

fig.update_layout(height=500, xaxis_title="Date", yaxis_title="Price (USD)")
st.plotly_chart(fig, use_container_width=True)

# Volume Chart
st.subheader("📈 Trading Volume")
fig_vol = go.Figure(data=[go.Bar(x=df.index, y=df['Volume'], name="Volume", marker_color='gray')])
fig_vol.update_layout(height=300, xaxis_title="Date", yaxis_title="Volume")
st.plotly_chart(fig_vol, use_container_width=True)
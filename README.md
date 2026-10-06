# Time Series Analysis & Forecasting for Apple (AAPL)

A time series analysis of Apple Inc. (AAPL) stock prices. The project downloads recent market data, explores it with interactive Plotly charts, fits SARIMAX models to the closing price, and evaluates forecasts against a naive baseline.

## Overview

The notebook pulls roughly the last 720 days of daily AAPL data from Yahoo Finance and visualizes price behavior in several ways. It then fits a SARIMAX model, checks its residual diagnostics, and tests how well a SARIMAX(1, 1, 1) model forecasts the most recent 30 trading days compared to a simple "tomorrow = today" baseline.

## Workflow

1. **Data collection**
   - Downloaded daily OHLCV data for `AAPL` with `yfinance`, covering the last 720 days up to the current date.
2. **Exploratory data analysis**
   - Inspected shape, data types, missing values, and summary statistics.
3. **Visualization (Plotly)**
   - Line plot of the closing price.
   - Candlestick chart.
   - Bar plot of the closing price.
   - Line plot with a custom date range.
   - Interactive candlestick chart with range selector buttons (1m, 6m, YTD, 1y, all) and a range slider.
4. **Modeling and diagnostics**
   - Fitted a SARIMAX(1, 0, 0) model on the closing price using `statsmodels`.
   - Reviewed the model summary and residual diagnostics.
5. **Forecasting**
   - Held out the last 30 trading days as a test set and trained SARIMAX(1, 1, 1) on the rest (the differencing term `d=1` handles the non-stationary price series).
   - Compared the forecast with a naive baseline (last known price repeated) using MAE, RMSE, and MAPE.
   - Plotted actual vs. forecast values with a 95% confidence interval.
   - Refit the model on the full data and produced a 30-business-day forward forecast.

## Results

### Model diagnostics (SARIMAX(1, 0, 0))

| Diagnostic | Value | Interpretation |
|------------|-------|----------------|
| AR(1) coefficient | ~0.9999 (p = 0.000) | Statistically significant, very strong persistence |
| Ljung-Box, Prob(Q) | 0.16 | No significant residual autocorrelation (white-noise-like residuals) |
| Heteroskedasticity, Prob(H) | 0.38 | No evidence of changing residual variance |
| Jarque-Bera, Prob(JB) | 0.00 | Residuals are not normally distributed |
| Kurtosis | 9.31 | Heavy tails |

### Forecast evaluation (last 30 trading days)

| Model | MAE | RMSE | MAPE (%) |
|-------|-----|------|----------|
| SARIMAX(1, 1, 1) | 18.749 | 20.935 | 5.642 |
| Naive baseline | 18.447 | 20.662 | 5.550 |

SARIMAX did not outperform the naive baseline; the two are nearly identical, with the baseline slightly ahead. This is consistent with the AR(1) coefficient being almost exactly 1: the closing price behaves like a random walk, so today's price is the best simple predictor of tomorrow's. A more complex model adds little over it at this horizon.

The numbers above come from one run of the notebook. Because data is downloaded at runtime, exact values change with the run date.

## Tech Stack

- Python
- pandas, NumPy
- yfinance
- statsmodels
- scikit-learn (error metrics)
- Plotly

## Getting Started

### Installation

```bash
git clone <your-repo-url>
cd <your-repo-folder>
pip install pandas numpy yfinance statsmodels scikit-learn plotly
```

### Data

No manual download is needed. The notebook fetches data from Yahoo Finance at runtime, so results change depending on the date you run it. An internet connection is required.

### Run

```bash
jupyter notebook TimeSeriesApple.ipynb
```

## Project Structure

```
.
├── TimeSeriesApple.ipynb   # Data download, EDA, visualization, modeling, and forecasting
└── README.md
```

## Possible Improvements

- Check stationarity with the ADF test and compare ARIMA/SARIMAX orders using AIC/BIC or `auto_arima`.
- Model returns or log-returns instead of raw prices.
- Use `seasonal_decompose` to examine trend and seasonality.
- Use rolling-origin (walk-forward) validation instead of a single train/test split.
- Compare against other approaches such as Prophet or LSTM.
- Model volatility with GARCH, given the heavy-tailed residuals.

## Disclaimer

This project is for educational purposes only and is not financial advice.

## Author

Furkan

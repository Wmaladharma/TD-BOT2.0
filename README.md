# SOL/USDT Futures Scalping Bot

This repository implements a modular real-time SOL/USDT futures analysis and signal-generation framework focused on short-horizon decision support. It follows a phased architecture that starts with exchange connectivity and the real-time market-data pipeline before adding analysis, prediction, risk management, backtesting, and optional paper/live execution.

## Final architecture

- Exchange and market data layer: public API + WebSocket feed, normalization, persistence.
- Indicator and feature layer: trend, momentum, volatility, order flow, market regime.
- Prediction layer: ML features, probabilistic forecast, path projection, confidence calibration.
- Signal engine: regime-aware strategy modules and ensemble scoring.
- Risk layer: position sizing, TP/SL, trade limits, micro-account checks.
- Notification layer: console, browser, desktop, and optional Telegram/Discord hooks.
- Backtesting and paper trading: walk-forward historical validation and simulated execution.
- Dashboard: real-time status, live signal display, prediction path, and risk metrics.

## Technology stack

- Python 3.11+
- pandas / numpy for market data and indicators
- scikit-learn for calibration and baseline ML models
- requests + websockets for exchange APIs and streaming
- SQLite for initial storage
- Streamlit for a dashboard prototype
- pytest for validation

## Data sources / API requirements

- Binance Futures REST API for public market data
- Binance Futures WebSocket streams for real-time price, kline, book, and trade updates
- Optional exchange-specific extras: funding, open interest, liquidation feed
- All API keys stay in .env and are never logged or committed

## Database design

SQLite is used initially with tables for:

- candles
- orderbook_snapshots
- trades
- funding
- open_interest
- predictions
- signals
- trade_results
- model_versions
- audit_logs

## ML approach

The system begins with interpretable models and probability calibration:

- Feature engineering from returns, EMA distances, RSI, MACD, ATR, VWAP, spread, OI, funding, CVD
- Baseline models: logistic regression and gradient boosting
- Calibration: isotonic or Platt scaling where available
- Output: direction probabilities across 1m, 3m, 5m, 10m and a projected path

## Strategy architecture

- TrendFollowingStrategy
- BreakoutStrategy
- MomentumStrategy
- MeanReversionStrategy
- ReversalStrategy
- OrderFlowStrategy
- Ensemble decision engine with confluence scoring and NO TRADE fallback

## Risk-management architecture

- account balance / micro-account checks
- risk per trade and daily loss caps
- stop-loss, take-profit, and R:R validation
- leverage and liquidation alerts
- minimum order size filtering
- cooldown after losses
- no martingale or revenge trading

## Dashboard architecture

- Top summary: SOL/USDT, price, funding, OI, volume
- Center chart: live candlesticks, indicators, predicted path, support/resistance
- Right panel: market state, signal, probability, TP/SL
- Bottom: activity log, live trades, prediction accuracy, system health

## Development phases

1. Exchange connectivity and market-data feed
2. Indicators and support/resistance
3. Order flow, OI, funding, liquidations
4. Regime detection and strategy modules
5. ML dataset, training, validation, calibration
6. 5m/10m prediction and confidence bands
7. Entry engine and TP/SL
8. Dashboard and notifications
9. Backtesting and walk-forward testing
10. Paper trading and optional live trading

## Testing methodology

- Unit tests for indicators and risk calculations
- Feature-level tests for market snapshots
- Probability calibration checks using simple score-to-probability mapping
- Trade validation for fees, minimum lot size, and PnL
- WebSocket reconnect health tests for missing or stale data
- Guardrails against look-ahead bias and future leakage in backtests

## Usage

```bash
pip install -r requirements.txt
python -m sol_scalper.app.main
```

> The dashboard and live trading path are designed to run in ANALYSIS mode by default. Live execution requires explicit configuration and confirmation.

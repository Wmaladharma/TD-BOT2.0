from __future__ import annotations

from sol_scalper.app.config import DEFAULT_CONFIG
from sol_scalper.data.collector import MarketDataCollector
from sol_scalper.dashboard.console_dashboard import ConsoleDashboard


def main() -> None:
    """Launch the market-data and dashboard loop in ANALYSIS mode by default."""
    config = DEFAULT_CONFIG
    collector = MarketDataCollector(symbol=config.symbol)
    dashboard = ConsoleDashboard()

    print(f"Mode: {config.mode} | Symbol: {config.symbol}")
    print("Starting data pipeline and dashboard...")

    snapshot = collector.get_market_snapshot()
    dashboard.render_snapshot(snapshot)

    print("System ready. Data pipeline connected in analysis mode.")


if __name__ == "__main__":
    main()

from __future__ import annotations

from sol_scalper.data.collector import MarketDataCollector

try:
    import streamlit as st
except ImportError:  # pragma: no cover
    st = None


def run_dashboard() -> None:
    if st is None:
        raise RuntimeError("streamlit is not installed")

    st.title("SOL/USDT Futures Signal Dashboard")
    collector = MarketDataCollector(symbol="SOLUSDT")
    snapshot = collector.get_market_snapshot()

    st.metric("Current price", f"${snapshot.price:.4f}")
    st.metric("Spread", f"${snapshot.spread:.4f}")
    st.metric("Funding", f"{snapshot.funding:.6f}")
    st.metric("Orderbook imbalance", f"{snapshot.orderbook_imbalance:.3f}")

    st.text(f"Last update: {snapshot.timestamp.isoformat()}")
    st.caption("This dashboard is intentionally conservative and analysis-first; live execution is disabled by default.")


if __name__ == "__main__":
    run_dashboard()

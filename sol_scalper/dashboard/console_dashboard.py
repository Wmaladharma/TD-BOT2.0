from __future__ import annotations

from sol_scalper.data.collector import MarketSnapshot


class ConsoleDashboard:
    """Simple dashboard output for the market snapshot and signal state."""

    def render_snapshot(self, snapshot: MarketSnapshot) -> None:
        print("=" * 60)
        print(f"SOL/USDT FUTURES | {snapshot.timestamp.isoformat()}")
        print(f"Price: ${snapshot.price:.4f}")
        print(f"Bid: ${snapshot.bid:.4f} | Ask: ${snapshot.ask:.4f} | Spread: ${snapshot.spread:.4f}")
        print(f"Volume: {snapshot.volume:,.2f} | Funding: {snapshot.funding:.6f} | OI: {snapshot.open_interest:,.2f}")
        print(f"Orderbook imbalance: {snapshot.orderbook_imbalance:.3f}")
        print("=" * 60)

        if snapshot.candles_1m:
            last = snapshot.candles_1m[-1]
            print(
                f"Latest 1m candle: O={last.open:.4f} H={last.high:.4f} "
                f"L={last.low:.4f} C={last.close:.4f} V={last.volume:.2f}"
            )

        if snapshot.candles_5m:
            last5 = snapshot.candles_5m[-1]
            print(
                f"Latest 5m candle: O={last5.open:.4f} H={last5.high:.4f} "
                f"L={last5.low:.4f} C={last5.close:.4f} V={last5.volume:.2f}"
            )

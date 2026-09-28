from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass
class MarketFeatureRow:
    timestamp: float
    close: float
    returns_1m: float
    returns_3m: float
    rsi_7: float
    rsi_14: float
    macd_hist: float
    atr: float
    vwap_distance: float
    volume_change: float
    orderbook_imbalance: float
    tradeflow_delta: float
    funding: float
    oi_change: float
    volatility: float
    trend_score: float
    target_label: int


class FeatureBuilder:
    """Build a compact, interpretable feature set for a directional SOLUSDT model."""

    def build(self, closes: Iterable[float], volumes: Iterable[float], rsi_7: float, rsi_14: float, macd_hist: float,
              atr: float, vwap: float, current_price: float, orderbook_imbalance: float, tradeflow_delta: float,
              funding: float, oi_change: float, volatility: float, trend_score: float) -> MarketFeatureRow:
        close_sequence = list(closes)
        if len(close_sequence) < 2:
            raise ValueError("Need at least two closes to compute return features")

        returns_1m = (close_sequence[-1] - close_sequence[-2]) / close_sequence[-2]
        returns_3m = (close_sequence[-1] - close_sequence[-3]) / close_sequence[-3] if len(close_sequence) >= 3 else returns_1m
        volume_sequence = list(volumes)
        volume_change = 0.0 if len(volume_sequence) < 2 else (volume_sequence[-1] - volume_sequence[-2]) / max(volume_sequence[-2], 1.0)
        vwap_distance = (current_price - vwap) / max(vwap, 1e-9)

        target_label = 1 if returns_1m > 0 else 0
        return MarketFeatureRow(
            timestamp=float(len(close_sequence)),
            close=float(close_sequence[-1]),
            returns_1m=float(returns_1m),
            returns_3m=float(returns_3m),
            rsi_7=float(rsi_7),
            rsi_14=float(rsi_14),
            macd_hist=float(macd_hist),
            atr=float(atr),
            vwap_distance=float(vwap_distance),
            volume_change=float(volume_change),
            orderbook_imbalance=float(orderbook_imbalance),
            tradeflow_delta=float(tradeflow_delta),
            funding=float(funding),
            oi_change=float(oi_change),
            volatility=float(volatility),
            trend_score=float(trend_score),
            target_label=int(target_label),
        )

    def as_array(self, row: MarketFeatureRow) -> np.ndarray:
        return np.asarray([
            row.returns_1m,
            row.returns_3m,
            row.rsi_7,
            row.rsi_14,
            row.macd_hist,
            row.atr,
            row.vwap_distance,
            row.volume_change,
            row.orderbook_imbalance,
            row.tradeflow_delta,
            row.funding,
            row.oi_change,
            row.volatility,
            row.trend_score,
        ], dtype=float)

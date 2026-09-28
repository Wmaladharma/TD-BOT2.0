from __future__ import annotations

from typing import Sequence

import numpy as np


def ema(values: Sequence[float], period: int) -> float:
    if not values:
        raise ValueError("values cannot be empty")
    if period <= 0:
        raise ValueError("period must be positive")
    multiplier = 2 / (period + 1)
    ema_value = float(values[0])
    for value in values[1:]:
        ema_value = (value - ema_value) * multiplier + ema_value
    return ema_value


def ema_series(values: Sequence[float], period: int) -> list[float]:
    if not values:
        return []
    multiplier = 2 / (period + 1)
    result: list[float] = []
    current = float(values[0])
    for value in values:
        current = (float(value) - current) * multiplier + current
        result.append(current)
    return result


def rsi(values: Sequence[float], period: int = 14) -> float:
    if len(values) < 2:
        return 50.0
    deltas = np.diff(np.asarray(values, dtype=float))
    gains = np.clip(deltas, 0, None)
    losses = np.clip(-deltas, 0, None)
    avg_gain = gains[:period].mean() if len(gains) >= period else gains.mean()
    avg_loss = losses[:period].mean() if len(losses) >= period else losses.mean()
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def macd(values: Sequence[float], fast: int = 12, slow: int = 26, signal: int = 9) -> dict[str, float]:
    if len(values) < slow:
        return {"macd": 0.0, "signal": 0.0, "histogram": 0.0}
    fast_ema = ema(values[-fast:], fast)
    slow_ema = ema(values[-slow:], slow)
    macd_value = fast_ema - slow_ema
    signal_value = macd_value
    histogram = macd_value - signal_value
    return {"macd": float(macd_value), "signal": float(signal_value), "histogram": float(histogram)}


def atr(high: Sequence[float], low: Sequence[float], close: Sequence[float], period: int = 14) -> float:
    if len(high) < 2:
        return 0.0
    true_ranges: list[float] = []
    for idx in range(1, len(close)):
        tr = max(
            high[idx] - low[idx],
            abs(high[idx] - close[idx - 1]),
            abs(low[idx] - close[idx - 1]),
        )
        true_ranges.append(tr)
    if not true_ranges:
        return 0.0
    return float(np.mean(true_ranges[-period:]))


def vwap(prices: Sequence[float], volumes: Sequence[float]) -> float:
    if not prices or not volumes:
        return 0.0
    p = np.asarray(prices, dtype=float)
    v = np.asarray(volumes, dtype=float)
    total = np.sum(p * v)
    denom = np.sum(v)
    return float(total / denom) if denom else 0.0


def bollinger_bands(values: Sequence[float], period: int = 20, std_dev: float = 2.0) -> dict[str, float]:
    if not values:
        return {"middle": 0.0, "upper": 0.0, "lower": 0.0}
    arr = np.asarray(values[-period:], dtype=float)
    mid = float(arr.mean())
    std = float(arr.std())
    return {"middle": mid, "upper": mid + std_dev * std, "lower": mid - std_dev * std}


def trend_bias(values: Sequence[float], period: int = 20) -> str:
    if len(values) < period:
        return "uncertain"
    recent = values[-period:]
    prev = values[-period - 1:-1]
    if not prev:
        return "uncertain"
    recent_avg = float(np.mean(recent))
    prev_avg = float(np.mean(prev))
    if recent_avg > prev_avg * 1.001:
        return "bullish"
    if recent_avg < prev_avg * 0.999:
        return "bearish"
    return "sideways"

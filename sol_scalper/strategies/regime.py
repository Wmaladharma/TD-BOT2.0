from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

import numpy as np


@dataclass
class RegimeResult:
    name: str
    strength: float
    confidence: float
    reasons: list[str] = field(default_factory=list)


class MultiTimeframeRegimeDetector:
    """Cheap and explainable multi-timeframe regime detection for SOL/USDT futures."""

    def __init__(self, min_strength: float = 0.15) -> None:
        self.min_strength = min_strength

    def detect(self, timeframe_closes: dict[str, Iterable[float]], volatility: float | None = None) -> RegimeResult:
        if not timeframe_closes:
            return RegimeResult(name="uncertain", strength=0.0, confidence=0.0, reasons=["No timeframes available"])

        scores: list[float] = []
        reasons: list[str] = []
        for tf, closes in timeframe_closes.items():
            arr = np.asarray(list(closes), dtype=float)
            if arr.size < 2:
                continue
            slope = float(np.polyfit(np.arange(arr.size), arr, 1)[0])
            slope_score = slope / max(float(np.std(arr)), 1e-9)
            scores.append(slope_score)
            if slope_score > 0.05:
                reasons.append(f"{tf} bullish slope")
            elif slope_score < -0.05:
                reasons.append(f"{tf} bearish slope")
            else:
                reasons.append(f"{tf} neutral")

        total = float(np.mean(scores)) if scores else 0.0
        vol = volatility if volatility is not None else max(abs(total) * 0.5, 0.05)

        if total > self.min_strength and vol < 0.6:
            return RegimeResult(name="strong_bullish", strength=abs(total), confidence=min(0.9, 0.55 + abs(total) * 0.8), reasons=reasons)
        if total > self.min_strength * 0.5:
            return RegimeResult(name="weak_bullish", strength=abs(total), confidence=min(0.8, 0.5 + abs(total) * 0.7), reasons=reasons)
        if total < -self.min_strength and vol < 0.6:
            return RegimeResult(name="strong_bearish", strength=abs(total), confidence=min(0.9, 0.55 + abs(total) * 0.8), reasons=reasons)
        if total < -self.min_strength * 0.5:
            return RegimeResult(name="weak_bearish", strength=abs(total), confidence=min(0.8, 0.5 + abs(total) * 0.7), reasons=reasons)
        if vol > 0.75:
            return RegimeResult(name="high_volatility", strength=0.5, confidence=0.5, reasons=["Volatility elevated; avoid forcing a trade"])
        return RegimeResult(name="range", strength=0.15, confidence=0.55, reasons=["Multi-timeframe structure is mixed or sideways"])

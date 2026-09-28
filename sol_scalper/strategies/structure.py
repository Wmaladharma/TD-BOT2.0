from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass
class SupportResistanceLevel:
    price: float
    kind: str
    strength: float
    touches: int
    last_touch: float | None = None


@dataclass
class BreakoutEvent:
    direction: str
    level: float
    confirmed: bool
    reason: str
    volume_surge: float = 0.0


class SupportResistanceEngine:
    """Calculate a simple support/resistance map from recent price history."""

    def detect_levels(self, closes: Iterable[float], highs: Iterable[float], lows: Iterable[float], tolerance: float = 0.01) -> list[SupportResistanceLevel]:
        closes = list(closes)
        highs = list(highs)
        lows = list(lows)
        if not closes:
            return []

        levels: list[SupportResistanceLevel] = []
        for idx, price in enumerate(closes):
            matches = False
            for level in levels:
                if abs(price - level.price) <= max(tolerance * price, 0.01):
                    level.touches += 1
                    level.strength = min(1.0, level.strength + 0.1)
                    level.last_touch = float(idx)
                    matches = True
                    break
            if not matches:
                levels.append(
                    SupportResistanceLevel(
                        price=float(price),
                        kind="support" if idx % 2 == 0 else "resistance",
                        strength=0.2,
                        touches=1,
                        last_touch=float(idx),
                    )
                )

        for level in levels:
            if level.kind == "support":
                level.strength = min(1.0, 0.2 + level.touches * 0.12)
            else:
                level.strength = min(1.0, 0.15 + level.touches * 0.1)
        return levels


class BreakoutDetector:
    """Detect likely breakouts with conservative confirmation checks."""

    def detect(self, last_close: float, recent_highs: list[float], recent_lows: list[float], volume_ratio: float, trend_bias: str, atr: float) -> BreakoutEvent | None:
        if not recent_highs or not recent_lows:
            return None
        local_high = max(recent_highs)
        local_low = min(recent_lows)
        if trend_bias == "bullish" and last_close > local_high * 1.001 and volume_ratio > 1.2 and atr > 0:
            return BreakoutEvent(direction="LONG", level=local_high, confirmed=True, reason="price closes above recent high with volume expansion", volume_surge=volume_ratio)
        if trend_bias == "bearish" and last_close < local_low * 0.999 and volume_ratio > 1.2 and atr > 0:
            return BreakoutEvent(direction="SHORT", level=local_low, confirmed=True, reason="price closes below recent low with volume expansion", volume_surge=volume_ratio)
        return BreakoutEvent(direction="WAIT", level=last_close, confirmed=False, reason="No confirmed breakout; insufficient momentum or volume", volume_surge=volume_ratio)

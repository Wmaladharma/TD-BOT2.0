from __future__ import annotations

from dataclasses import dataclass


@dataclass
class StrategySignal:
    name: str
    direction: str
    score: float
    reason: str


class SignalEngine:
    """Create a realistic ensemble signal with a distinct WAIT / NO TRADE fallback."""

    def __init__(self, min_confidence: float = 0.7, min_signal_count: int = 2) -> None:
        self.min_confidence = min_confidence
        self.min_signal_count = min_signal_count

    def combine(self, signals: list[StrategySignal]) -> tuple[str, float, str, str]:
        if not signals:
            return "WAIT", 0.0, "NO TRADE", "No strategy signals available"

        bullish = [signal for signal in signals if signal.direction == "LONG"]
        bearish = [signal for signal in signals if signal.direction == "SHORT"]

        if len(bullish) >= self.min_signal_count and len(bearish) == 0:
            confidence = min(0.99, sum(signal.score for signal in bullish) / max(len(bullish), 1))
            if confidence < self.min_confidence:
                return "WAIT", confidence, "NO TRADE", "Bullish signal strength is below required threshold"
            return "LONG", confidence, "HIGH CONFLUENCE", "Multiple bullish signals agree"

        if len(bearish) >= self.min_signal_count and len(bullish) == 0:
            confidence = min(0.99, sum(signal.score for signal in bearish) / max(len(bearish), 1))
            if confidence < self.min_confidence:
                return "WAIT", confidence, "NO TRADE", "Bearish signal strength is below required threshold"
            return "SHORT", confidence, "HIGH CONFLUENCE", "Multiple bearish signals agree"

        if len(bullish) > 0 and len(bearish) > 0:
            long_score = sum(signal.score for signal in bullish)
            short_score = sum(signal.score for signal in bearish)
            if long_score > short_score:
                confidence = min(0.99, long_score / max(long_score + short_score, 1e-9))
                if confidence < self.min_confidence:
                    return "WAIT", confidence, "NO TRADE", "Conflicting signals and poor confidence"
                return "LONG", confidence, "WAIT", "Bullish signal marginally leads"
            if short_score > long_score:
                confidence = min(0.99, short_score / max(long_score + short_score, 1e-9))
                if confidence < self.min_confidence:
                    return "WAIT", confidence, "NO TRADE", "Conflicting signals and poor confidence"
                return "SHORT", confidence, "WAIT", "Bearish signal marginally leads"

        return "WAIT", 0.0, "NO TRADE", "Market structure is neutral or conflicted"

    def classify_strength(self, confidence: float) -> str:
        if confidence >= 0.8:
            return "Very strong"
        if confidence >= 0.7:
            return "Strong"
        if confidence >= 0.6:
            return "Moderate"
        if confidence >= 0.5:
            return "Weak"
        return "No trade"

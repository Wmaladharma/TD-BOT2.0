from __future__ import annotations

from dataclasses import dataclass


@dataclass
class OrderBookPressure:
    imbalance: float
    pressure: str
    bid_volume: float
    ask_volume: float


class OrderBookAnalyzer:
    """Analyze bid/ask depth imbalances and classify pressure."""

    def analyze(self, bid_volume: float, ask_volume: float) -> dict[str, float | str]:
        total = bid_volume + ask_volume
        if total <= 0:
            return {"imbalance": 0.0, "pressure": "NEUTRAL", "bid_volume": bid_volume, "ask_volume": ask_volume}
        imbalance = (bid_volume - ask_volume) / total
        if imbalance > 0.1:
            pressure = "BUYING_PRESSURE"
        elif imbalance < -0.1:
            pressure = "SELLING_PRESSURE"
        else:
            pressure = "NEUTRAL"
        return {"imbalance": imbalance, "pressure": pressure, "bid_volume": bid_volume, "ask_volume": ask_volume}


class TradeFlowAnalyzer:
    """Analyze aggressive trade flow and volume delta."""

    def aggregate_delta(self, buy_volume: float, sell_volume: float) -> float:
        return buy_volume - sell_volume

    def classify(self, buy_volume: float, sell_volume: float) -> str:
        delta = self.aggregate_delta(buy_volume, sell_volume)
        if delta > 0:
            return "AGGRESSIVE_BUYING"
        if delta < 0:
            return "AGGRESSIVE_SELLING"
        return "BALANCED"

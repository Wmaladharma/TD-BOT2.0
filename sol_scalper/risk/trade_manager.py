from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TradePlan:
    direction: str
    entry: float
    tp: float
    sl: float
    expected_net_profit: float
    confidence: float
    rr: float
    status: str = "ACTIVE"


class TradeManager:
    """Conservative trade management layer. This does not auto-escalate after losses."""

    def __init__(self, max_daily_loss: float = 0.05, cooldown_minutes: int = 15) -> None:
        self.max_daily_loss = max_daily_loss
        self.cooldown_minutes = cooldown_minutes
        self.loss_streak = 0

    def build_trade_plan(self, direction: str, entry: float, atr: float, risk_reward: float = 1.8, confidence: float = 0.7) -> TradePlan:
        if direction not in {"LONG", "SHORT"}:
            raise ValueError("direction must be LONG or SHORT")
        stop_distance = max(atr * 0.8, 0.01 * entry)
        if direction == "LONG":
            tp = entry + stop_distance * risk_reward
            sl = entry - stop_distance
        else:
            tp = entry - stop_distance * risk_reward
            sl = entry + stop_distance
        rr = abs((tp - entry) / (entry - sl)) if entry != sl else 0.0
        expected_net_profit = max(0.0, abs(tp - entry) - 2e-4 * entry)
        return TradePlan(direction=direction, entry=entry, tp=tp, sl=sl, expected_net_profit=expected_net_profit, confidence=confidence, rr=max(rr, 0.0))

    def record_loss(self) -> None:
        self.loss_streak += 1

    def can_trade(self, elapsed_minutes_since_last_trade: int) -> bool:
        return elapsed_minutes_since_last_trade >= self.cooldown_minutes and self.loss_streak < 3

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EntryPlan:
    direction: str
    entry: float
    tp: float
    sl: float
    confidence: float
    rr: float
    expected_net_profit: float
    expected_hold_minutes: tuple[int, int]
    reason: str
    valid: bool = True


class EntryEngine:
    """Generate conservative entry plans only when multiple checks agree."""

    def __init__(self, min_confidence: float = 0.7, min_rr: float = 1.5, fee_rate: float = 0.0005, slippage: float = 0.0003) -> None:
        self.min_confidence = min_confidence
        self.min_rr = min_rr
        self.fee_rate = fee_rate
        self.slippage = slippage

    def generate(self, price: float, regime: str, trend: str, momentum: str, orderflow: str, breakout: str,
                 ml_probability: float, atr: float, expected_move: float, risk_cap: float = 0.01) -> EntryPlan:
        score = 0.0
        reasons: list[str] = []

        if regime in {"strong_bullish", "weak_bullish"}:
            score += 0.2
            reasons.append("higher timeframe bullish")
        if trend == "bullish":
            score += 0.15
            reasons.append("short-term trend aligned")
        if momentum == "bullish":
            score += 0.15
            reasons.append("momentum supports upside")
        if orderflow == "BUYING_PRESSURE":
            score += 0.2
            reasons.append("order flow positive")
        if breakout == "LONG":
            score += 0.2
            reasons.append("breakout confirmed")

        confidence = min(0.99, max(0.0, score + ml_probability * 0.35))
        if confidence < self.min_confidence:
            return EntryPlan(direction="WAIT", entry=price, tp=price, sl=price, confidence=confidence, rr=0.0,
                             expected_net_profit=0.0, expected_hold_minutes=(0, 0), reason="Insufficient confirmation.", valid=False)

        stop_distance = max(atr * 0.8, price * 0.003)
        if confidence >= self.min_confidence:
            direction = "LONG"
            entry = price
            tp = price + stop_distance * self.min_rr
            sl = price - stop_distance
            rr = (tp - entry) / max(entry - sl, 1e-9)
            fees = (entry * self.fee_rate) + (tp * self.fee_rate) + (price * self.slippage)
            expected_net_profit = max(0.0, (tp - entry) - fees)
            if expected_net_profit <= 0:
                return EntryPlan(direction="WAIT", entry=entry, tp=tp, sl=sl, confidence=confidence, rr=rr,
                                 expected_net_profit=expected_net_profit, expected_hold_minutes=(3, 7),
                                 reason="Expected net profit too low after fees and slippage", valid=False)
            return EntryPlan(direction="LONG", entry=entry, tp=tp, sl=sl, confidence=confidence, rr=rr,
                             expected_net_profit=expected_net_profit, expected_hold_minutes=(3, 7),
                             reason="; ".join(reasons) if reasons else "Bullish confluence")

        direction = "SHORT"
        entry = price
        tp = price - stop_distance * self.min_rr
        sl = price + stop_distance
        rr = (entry - tp) / max(sl - entry, 1e-9)
        fees = (entry * self.fee_rate) + (tp * self.fee_rate) + (price * self.slippage)
        expected_net_profit = max(0.0, (entry - tp) - fees)
        if expected_net_profit <= 0:
            return EntryPlan(direction="WAIT", entry=entry, tp=tp, sl=sl, confidence=confidence, rr=rr,
                             expected_net_profit=expected_net_profit, expected_hold_minutes=(3, 7),
                             reason="Expected net profit too low after fees and slippage", valid=False)
        return EntryPlan(direction="SHORT", entry=entry, tp=tp, sl=sl, confidence=confidence, rr=rr,
                         expected_net_profit=expected_net_profit, expected_hold_minutes=(3, 7),
                         reason="; ".join(reasons) if reasons else "Bearish confluence")

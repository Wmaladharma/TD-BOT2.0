from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TradeState:
    symbol: str = "SOLUSDT"
    direction: str = "WAIT"
    entry: float = 0.0
    tp: float = 0.0
    sl: float = 0.0
    confidence: float = 0.0
    expected_net_profit: float = 0.0
    status: str = "ACTIVE"
    reason: str = ""
    expires_at: float = 0.0


@dataclass
class SignalState:
    direction: str = "WAIT"
    confidence: float = 0.0
    entry: float = 0.0
    tp: float = 0.0
    sl: float = 0.0
    rationale: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    signal_valid_for_seconds: int = 45
    mode: str = "CONFIRMED"

    def to_trade_state(self, symbol: str = "SOLUSDT") -> TradeState:
        return TradeState(
            symbol=symbol,
            direction=self.direction,
            entry=self.entry,
            tp=self.tp,
            sl=self.sl,
            confidence=self.confidence,
            status="ACTIVE",
            reason="; ".join(self.rationale) if self.rationale else "signal generated",
            expires_at=float(self.signal_valid_for_seconds),
        )

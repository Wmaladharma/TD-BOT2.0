from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PositionSizing:
    account_balance: float
    risk_percent: float
    stop_distance: float
    leverage: float = 1.0
    entry_price: float = 0.0
    min_notional: float = 0.0

    @property
    def max_risk_amount(self) -> float:
        return self.account_balance * self.risk_percent

    @property
    def position_size(self) -> float:
        if self.stop_distance <= 0:
            return 0.0
        raw_size = self.max_risk_amount / self.stop_distance
        if self.entry_price > 0:
            return raw_size / self.entry_price
        return raw_size

    @property
    def notional_value(self) -> float:
        return self.position_size * self.entry_price if self.entry_price > 0 else 0.0

    @property
    def leverage_used(self) -> float:
        if self.notional_value <= 0:
            return 0.0
        return self.notional_value / max(self.account_balance, 1e-9)

    def validate(self) -> tuple[bool, str]:
        if self.min_notional > 0 and self.notional_value < self.min_notional:
            return False, "minimum order requirement not met"
        if self.position_size <= 0:
            return False, "position size is zero or negative"
        return True, "ok"


def calculate_position_size(account_balance: float, risk_percent: float, stop_distance: float, entry_price: float, leverage: float = 1.0, min_notional: float = 0.0) -> PositionSizing:
    return PositionSizing(
        account_balance=account_balance,
        risk_percent=risk_percent,
        stop_distance=stop_distance,
        leverage=leverage,
        entry_price=entry_price,
        min_notional=min_notional,
    )


def expected_net_profit(entry: float, tp: float, sl: float, account_balance: float, fee_rate: float = 0.0005, slippage: float = 0.0005) -> float:
    gross_profit = tp - entry
    costs = (entry + tp) * fee_rate + (entry * slippage) + (tp * slippage)
    net = gross_profit - costs
    if sl >= entry:
        net = -((entry - sl) + account_balance * 0.01)
    return net

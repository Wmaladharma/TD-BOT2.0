from __future__ import annotations


def calculate_tp_sl(entry: float, atr: float, rr: float = 1.8, volatility_buffer: float = 0.15) -> tuple[float, float]:
    if atr <= 0:
        atr = 0.01 * entry
    stop = atr * 0.9
    take_profit = stop * rr + (atr * volatility_buffer / 100)
    return entry - stop, entry + take_profit


def net_expected_profit(entry: float, tp: float, sl: float, fee_rate: float = 0.0008) -> float:
    gross = tp - entry
    fee = max(abs(tp - entry), abs(entry - sl)) * fee_rate
    return gross - fee

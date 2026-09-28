from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SignalDisplay:
    symbol: str
    state: str
    price: float
    confidence: float
    direction: str
    entry: float
    tp: float
    sl: float
    rr: float
    reason: str
    valid_for_seconds: int = 45


class SignalDashboard:
    """Render a compact signal summary suitable for console and UI display."""

    def render(self, signal: SignalDisplay) -> str:
        return (
            f"{signal.symbol} | {signal.state} | {signal.direction} | Price=${signal.price:.4f} | "
            f"Confidence={signal.confidence:.2%} | Entry=${signal.entry:.4f} | TP=${signal.tp:.4f} | "
            f"SL=${signal.sl:.4f} | R:R={signal.rr:.2f} | Valid={signal.valid_for_seconds}s | "
            f"Reason={signal.reason}"
        )

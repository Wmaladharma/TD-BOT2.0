from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BacktestResult:
    n_trades: int
    total_return: float
    final_equity: float
    win_rate: float
    max_drawdown: float


class BacktestEngine:
    """Minimal historical backtest runner with fee and slippage assumptions."""

    def run(self, closes: list[float], fee_rate: float = 0.0005, slippage: float = 0.0003) -> dict[str, float | int]:
        if len(closes) < 2:
            return {"n_trades": 0, "total_return": 0.0, "final_equity": 1.0, "win_rate": 0.0, "max_drawdown": 0.0}

        equity = 1.0
        n_trades = 0
        wins = 0
        drawdown = 0.0
        peak = equity

        for idx in range(1, len(closes)):
            ret = (closes[idx] - closes[idx - 1]) / closes[idx - 1]
            if abs(ret) > 0.0005:
                n_trades += 1
                trade_return = ret - fee_rate - slippage
                if trade_return > 0:
                    wins += 1
                equity *= 1 + trade_return
                peak = max(peak, equity)
                drawdown = max(drawdown, (peak - equity) / peak if peak > 0 else 0.0)

        win_rate = wins / n_trades if n_trades else 0.0
        return {
            "n_trades": n_trades,
            "total_return": equity - 1.0,
            "final_equity": equity,
            "win_rate": win_rate,
            "max_drawdown": drawdown,
        }

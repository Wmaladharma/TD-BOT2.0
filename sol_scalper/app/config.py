from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal

from dotenv import load_dotenv

load_dotenv()

Mode = Literal["ANALYSIS", "PAPER", "LIVE"]


@dataclass(frozen=True)
class AppConfig:
    mode: Mode = os.getenv("MODE", "ANALYSIS").upper()
    symbol: str = os.getenv("TRADING_PAIR", "SOLUSDT")
    prediction_horizon: int = int(os.getenv("PREDICTION_HORIZON", "5"))
    min_confidence: float = float(os.getenv("MIN_CONFIDENCE", "0.70"))
    min_rr: float = float(os.getenv("MIN_RR", "1.5"))
    max_risk_per_trade: float = float(os.getenv("MAX_RISK_PER_TRADE", "0.01"))
    max_daily_loss: float = float(os.getenv("MAX_DAILY_LOSS", "0.05"))
    leverage: float = float(os.getenv("LEVERAGE", "3"))
    paper_trading: bool = os.getenv("PAPER_TRADING", "ON").upper() == "ON"
    live_trading: bool = os.getenv("LIVE_TRADING", "OFF").upper() == "ON"
    notifications: bool = os.getenv("NOTIFICATIONS", "ON").upper() == "ON"
    api_key: str = os.getenv("API_KEY", "")
    api_secret: str = os.getenv("API_SECRET", "")

    @property
    def is_live_enabled(self) -> bool:
        return self.mode == "LIVE" and self.live_trading and bool(self.api_key)


DEFAULT_CONFIG = AppConfig()

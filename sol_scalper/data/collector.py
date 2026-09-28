from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

import pandas as pd
import requests


@dataclass
class Candle:
    open_time: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass
class MarketSnapshot:
    symbol: str
    timestamp: datetime
    price: float
    bid: float
    ask: float
    spread: float
    volume: float
    funding: float = 0.0
    open_interest: float = 0.0
    candles_1m: list[Candle] = field(default_factory=list)
    candles_5m: list[Candle] = field(default_factory=list)
    orderbook_imbalance: float = 0.0
    trade_flow_imbalance: float = 0.0


class MarketDataCollector:
    """Collect market data from the exchange REST API for SOL/USDT futures."""

    def __init__(self, symbol: str = "SOLUSDT", base_url: str = "https://fapi.binance.com") -> None:
        self.symbol = symbol
        self.base_url = base_url

    def get_market_snapshot(self) -> MarketSnapshot:
        ticker = self._get_json(f"/fapi/v1/ticker/24hr?symbol={self.symbol}")
        book = self._get_json(f"/fapi/v1/depth?symbol={self.symbol}&limit=20")
        klines_1m = self._get_json(f"/fapi/v1/klines?symbol={self.symbol}&interval=1m&limit=100")
        klines_5m = self._get_json(f"/fapi/v1/klines?symbol={self.symbol}&interval=5m&limit=100")
        funding = self._get_json(f"/fapi/v1/fundingRate?symbol={self.symbol}")
        oi = self._get_json(f"/fapi/v1/openInterest?symbol={self.symbol}")

        price = float(ticker["lastPrice"])
        bids = book.get("bids", [])
        asks = book.get("asks", [])
        bid_qty = sum(float(level[1]) for level in bids[:10])
        ask_qty = sum(float(level[1]) for level in asks[:10])
        imbalance = 0.0 if (bid_qty + ask_qty) == 0 else (bid_qty - ask_qty) / (bid_qty + ask_qty)

        snapshot = MarketSnapshot(
            symbol=self.symbol,
            timestamp=datetime.now(timezone.utc),
            price=price,
            bid=float(bids[0][0]) if bids else price,
            ask=float(asks[0][0]) if asks else price,
            spread=(float(asks[0][0]) - float(bids[0][0])) if bids and asks else 0.0,
            volume=float(ticker["quoteVolume"]),
            funding=float(funding[0]["fundingRate"]) if isinstance(funding, list) and funding else 0.0,
            open_interest=float(oi.get("openInterest", 0.0)) if isinstance(oi, dict) else 0.0,
            candles_1m=self._parse_klines(klines_1m),
            candles_5m=self._parse_klines(klines_5m),
            orderbook_imbalance=imbalance,
        )
        return snapshot

    def _parse_klines(self, klines: list[list[Any]]) -> list[Candle]:
        candles: list[Candle] = []
        for k in klines:
            candles.append(
                Candle(
                    open_time=pd.to_datetime(k[0], unit="ms", utc=True).to_pydatetime(),
                    open=float(k[1]),
                    high=float(k[2]),
                    low=float(k[3]),
                    close=float(k[4]),
                    volume=float(k[5]),
                )
            )
        return candles

    def _get_json(self, endpoint: str) -> Any:
        response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
        response.raise_for_status()
        return response.json()

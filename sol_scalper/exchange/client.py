from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ExchangeClient(ABC):
    """Abstract exchange client for SOL/USDT perp futures data and orders."""

    @abstractmethod
    def get_ticker(self, symbol: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_klines(self, symbol: str, interval: str, limit: int = 100) -> list[list[Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_orderbook(self, symbol: str, limit: int = 20) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_recent_trades(self, symbol: str, limit: int = 20) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_open_interest(self, symbol: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_funding_rate(self, symbol: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_positions(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_balance(self) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def place_order(self, symbol: str, side: str, quantity: float, price: float | None = None) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def cancel_order(self, order_id: str, symbol: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_order_status(self, order_id: str, symbol: str) -> dict[str, Any]:
        raise NotImplementedError

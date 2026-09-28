from __future__ import annotations

import asyncio
import json
from typing import Any, Callable

import websockets


class ExchangeWebSocket:
    """Minimal WebSocket client wrapper with reconnect logic and message dispatch."""

    def __init__(self, url: str, message_handler: Callable[[dict[str, Any]], None] | None = None) -> None:
        self.url = url
        self.message_handler = message_handler or (lambda message: None)
        self._connected = False

    async def connect(self) -> None:
        while True:
            try:
                async with websockets.connect(self.url) as websocket:
                    self._connected = True
                    async for raw in websocket:
                        if not raw:
                            continue
                        message = json.loads(raw)
                        self.message_handler(message)
            except Exception:
                self._connected = False
                await asyncio.sleep(2)

    async def subscribe(self, stream_name: str, params: dict[str, Any]) -> None:
        payload = {"method": "SUBSCRIBE", "params": [f"{stream_name}@{params['topic']}"], "id": 1}
        # This hook is intentionally lightweight; the actual exchange-specific stream configuration
        # should be adjusted per broker/API in production.
        self.last_subscription = payload

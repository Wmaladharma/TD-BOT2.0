from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Notification:
    title: str
    message: str
    level: str = "INFO"


class NotificationEngine:
    """Simple notification routing; expands to browser/desktop/Telegram later."""

    def __init__(self, enabled: bool = True) -> None:
        self.enabled = enabled

    def send(self, notification: Notification) -> bool:
        if not self.enabled:
            return False
        print(f"[{notification.level}] {notification.title}: {notification.message}")
        return True

    def entry_opportunity(self, symbol: str, entry: float, tp: float, sl: float, confidence: float) -> bool:
        return self.send(Notification(title=f"{symbol} ENTRY", message=f"Entry=${entry:.4f}, TP=${tp:.4f}, SL=${sl:.4f}, Confidence={confidence:.2%}", level="ALERT"))

    def invalidated(self, reason: str) -> bool:
        return self.send(Notification(title="SIGNAL INVALIDATED", message=reason, level="WARN"))

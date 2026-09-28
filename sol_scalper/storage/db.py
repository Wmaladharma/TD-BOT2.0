from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from typing import Any


class SQLiteStore:
    """Minimal SQLite persistence for signals and audit events."""

    def __init__(self, db_path: str = "sol_scalper.db") -> None:
        self.db_path = db_path
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _initialize(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS signals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    direction TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    price REAL NOT NULL,
                    entry REAL,
                    sl REAL,
                    tp REAL,
                    reason TEXT,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    actor TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    payload TEXT,
                    created_at TEXT NOT NULL
                )
                """
            )

    def save_signal(
        self,
        symbol: str,
        direction: str,
        confidence: float,
        price: float,
        entry: float | None,
        sl: float | None,
        tp: float | None,
        reason: str | None = None,
    ) -> int:
        created_at = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO signals (symbol, direction, confidence, price, entry, sl, tp, reason, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (symbol, direction, float(confidence), float(price), entry, sl, tp, reason, created_at),
            )
            return int(cursor.lastrowid)

    def latest_signal(self) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM signals ORDER BY id DESC LIMIT 1"
            ).fetchone()
            return dict(row) if row is not None else None

    def log_event(self, actor: str, event_type: str, payload: dict[str, Any] | None = None) -> int:
        created_at = datetime.now(timezone.utc).isoformat()
        payload_json = json.dumps(payload or {})
        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO audit_logs (actor, event_type, payload, created_at) VALUES (?, ?, ?, ?)",
                (actor, event_type, payload_json, created_at),
            )
            return int(cursor.lastrowid)

    def recent_events(self, limit: int = 20) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM audit_logs ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [
            {
                "id": row["id"],
                "actor": row["actor"],
                "event_type": row["event_type"],
                "payload": json.loads(row["payload"] or "{}"),
                "created_at": row["created_at"],
            }
            for row in rows
        ]

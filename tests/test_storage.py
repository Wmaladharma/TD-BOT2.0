from pathlib import Path

from sol_scalper.storage.db import SQLiteStore


def test_sqlite_store_persists_signal_and_audit(tmp_path: Path):
    db_path = tmp_path / "sol_signal.db"
    store = SQLiteStore(str(db_path))

    store.save_signal("SOLUSDT", "LONG", 0.82, 210.5, 211.2, 209.8, "trend continuation")
    store.log_event("SYSTEM", "analysis_start", {"mode": "ANALYSIS"})

    row = store.latest_signal()
    assert row is not None
    assert row["symbol"] == "SOLUSDT"
    assert row["direction"] == "LONG"

    events = store.recent_events(limit=5)
    assert any(event["event_type"] == "analysis_start" for event in events)

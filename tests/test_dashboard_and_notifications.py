from sol_scalper.dashboard.signal_dashboard import SignalDashboard, SignalDisplay
from sol_scalper.notifications.engine import Notification, NotificationEngine


def test_signal_dashboard_renders_summary():
    dashboard = SignalDashboard()
    text = dashboard.render(
        SignalDisplay(
            symbol="SOLUSDT",
            state="LONG",
            price=210.5,
            confidence=0.74,
            direction="LONG",
            entry=210.45,
            tp=211.0,
            sl=209.9,
            rr=2.1,
            reason="bullish trend",
        )
    )
    assert "SOLUSDT" in text
    assert "LONG" in text
    assert "Confidence=74.00%" in text


def test_notification_engine_sends_alert():
    engine = NotificationEngine(enabled=True)
    note = Notification(title="ENTRY", message="Long setup", level="ALERT")
    assert engine.send(note) is True

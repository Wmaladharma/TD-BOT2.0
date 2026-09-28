from sol_scalper.data.collector import MarketDataCollector
from sol_scalper.indicators.engine import atr, ema, rsi
from sol_scalper.risk.position_size import calculate_position_size
from sol_scalper.strategies.ensemble import SignalEngine, StrategySignal


def test_ema_works_on_simple_sequence():
    values = [10, 11, 12, 13, 14]
    assert ema(values, 3) > 10
    assert ema(values, 3) < 14


def test_rsi_returns_reasonable_range():
    values = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
    assert 0 <= rsi(values, 7) <= 100


def test_atr_returns_positive_value():
    high = [100, 101, 102, 103]
    low = [99, 100, 101, 102]
    close = [99.5, 100.5, 101.8, 102.7]
    assert atr(high, low, close, period=2) > 0


def test_position_size_validates_without_min_notional():
    sizing = calculate_position_size(
        account_balance=10.0,
        risk_percent=0.01,
        stop_distance=0.20,
        entry_price=200.0,
        leverage=3.0,
        min_notional=0.0,
    )
    assert sizing.max_risk_amount > 0
    assert sizing.position_size > 0
    valid, reason = sizing.validate()
    assert valid and reason == "ok"


def test_signal_engine_rejects_conflicting_low_confidence_signals():
    engine = SignalEngine(min_confidence=0.7)
    result = engine.combine([
        StrategySignal(name="trend", direction="LONG", score=0.52, reason="bullish"),
        StrategySignal(name="flow", direction="SHORT", score=0.48, reason="bearish"),
    ])
    assert result[0] == "WAIT"


def test_parse_klines_converts_binance_format():
    collector = MarketDataCollector(symbol="SOLUSDT")
    klines = [
        [1710000000000, "210.0", "212.0", "209.0", "211.0", "5000", 0, 0, 0, 0, 0, 0],
        [1710000001000, "211.0", "213.5", "210.5", "212.8", "6000", 0, 0, 0, 0, 0, 0],
    ]
    candles = collector._parse_klines(klines)
    assert len(candles) == 2
    assert candles[0].open == 210.0
    assert candles[-1].close == 212.8

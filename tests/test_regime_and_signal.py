from sol_scalper.prediction.confidence import ProbabilityCalibrator
from sol_scalper.risk.trade_manager import TradeManager
from sol_scalper.strategies.ensemble import SignalEngine, StrategySignal
from sol_scalper.strategies.regime import MultiTimeframeRegimeDetector


def test_regime_detector_identifies_bullish_market():
    detector = MultiTimeframeRegimeDetector(min_strength=0.1)
    regime = detector.detect({
        "1m": [100.0, 100.5, 101.0, 101.6],
        "5m": [99.5, 100.0, 100.8, 101.3],
        "15m": [98.8, 99.6, 100.3, 101.0],
    }, volatility=0.2)
    assert regime.name in {"strong_bullish", "weak_bullish"}


def test_probability_calibrator_keeps_probabilities_conservative():
    calibrator = ProbabilityCalibrator(model_score=0.75)
    probs = calibrator.calibrate()
    assert 0.0 <= probs.long <= 1.0
    assert 0.0 <= probs.short <= 1.0
    assert 0.0 <= probs.neutral <= 1.0
    assert abs((probs.long + probs.short + probs.neutral) - 1.0) < 1e-6


def test_trade_manager_blocks_reentry_after_losses():
    manager = TradeManager(max_daily_loss=0.05, cooldown_minutes=15)
    manager.record_loss()
    manager.record_loss()
    assert manager.can_trade(10) is False


def test_signal_engine_returns_wait_on_conflicts():
    engine = SignalEngine(min_confidence=0.7)
    result = engine.combine([
        StrategySignal(name="trend", direction="LONG", score=0.55, reason="trend"),
        StrategySignal(name="flow", direction="SHORT", score=0.45, reason="flow"),
    ])
    assert result[0] == "WAIT"
    assert result[2] == "NO TRADE"

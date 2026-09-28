from sol_scalper.strategies.structure import BreakoutDetector, SupportResistanceEngine


def test_support_resistance_levels_are_generated():
    engine = SupportResistanceEngine()
    levels = engine.detect_levels(
        closes=[100.0, 100.3, 100.1, 100.5, 100.6, 100.4, 100.7],
        highs=[100.8, 100.9, 100.5, 100.7, 101.0, 100.6, 100.9],
        lows=[99.7, 99.9, 99.8, 100.0, 100.2, 100.1, 100.3],
    )
    assert len(levels) > 0
    assert all(level.strength > 0 for level in levels)


def test_breakout_detector_flags_confident_breakout():
    detector = BreakoutDetector()
    event = detector.detect(
        last_close=101.8,
        recent_highs=[100.9, 101.0, 101.2, 101.4],
        recent_lows=[99.7, 99.8, 99.9, 100.4],
        volume_ratio=1.6,
        trend_bias="bullish",
        atr=0.3,
    )
    assert event is not None
    assert event.confirmed is True
    assert event.direction == "LONG"

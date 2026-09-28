from sol_scalper.strategies.entry_engine import EntryEngine


def test_entry_engine_generates_valid_long_plan():
    engine = EntryEngine(min_confidence=0.7, min_rr=1.5)
    plan = engine.generate(
        price=210.0,
        regime="strong_bullish",
        trend="bullish",
        momentum="bullish",
        orderflow="BUYING_PRESSURE",
        breakout="LONG",
        ml_probability=0.78,
        atr=0.35,
        expected_move=0.5,
    )
    assert plan.valid is True
    assert plan.direction == "LONG"
    assert plan.tp > plan.entry
    assert plan.sl < plan.entry
    assert plan.confidence >= 0.7


def test_entry_engine_rejects_low_confidence_setup():
    engine = EntryEngine(min_confidence=0.7, min_rr=1.5)
    plan = engine.generate(
        price=210.0,
        regime="range",
        trend="sideways",
        momentum="neutral",
        orderflow="NEUTRAL",
        breakout="WAIT",
        ml_probability=0.42,
        atr=0.3,
        expected_move=0.05,
    )
    assert plan.valid is False
    assert plan.direction == "WAIT"

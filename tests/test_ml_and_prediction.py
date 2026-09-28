from sol_scalper.ml.dataset import FeatureBuilder
from sol_scalper.ml.model import DirectionalModel
from sol_scalper.prediction.path import PathPredictor


def test_feature_builder_creates_reasonable_row():
    builder = FeatureBuilder()
    row = builder.build(
        closes=[100.0, 100.4, 100.8, 101.0],
        volumes=[1000.0, 1200.0, 1100.0, 1500.0],
        rsi_7=55.0,
        rsi_14=58.0,
        macd_hist=0.25,
        atr=0.3,
        vwap=100.0,
        current_price=101.0,
        orderbook_imbalance=0.15,
        tradeflow_delta=50.0,
        funding=0.0001,
        oi_change=0.05,
        volatility=0.02,
        trend_score=0.6,
    )
    assert row.target_label in {0, 1}
    assert row.returns_1m != 0


def test_directional_model_predicts():
    model = DirectionalModel()
    X = [
        [0.01, 0.02, 55.0, 58.0, 0.2, 0.3, 0.01, 0.1, 0.1, 20.0, 0.0001, 0.05, 0.02, 0.6],
        [-0.01, -0.02, 45.0, 48.0, -0.2, 0.4, 0.02, -0.1, -0.1, -15.0, -0.0001, -0.05, 0.03, -0.4],
    ]
    y = [1, 0]
    model.fit(X, y)
    prediction = model.predict(X[0], expected_return=0.01)
    assert prediction.direction in {"UP", "DOWN"}
    assert 0.0 <= prediction.probability <= 1.0


def test_path_predictor_generates_points():
    predictor = PathPredictor()
    path = predictor.predict(100.0, base_return=0.003, direction="LONG", horizon_minutes=5)
    assert len(path.points) == 5
    assert path.points[0].minute == 1
    assert path.expected_return > 0

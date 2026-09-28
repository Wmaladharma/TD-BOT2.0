from sol_scalper.backtesting.engine import BacktestEngine
from sol_scalper.orderflow.analysis import OrderBookAnalyzer, TradeFlowAnalyzer


def test_orderbook_analyzer_reports_imbalance_direction():
    analyzer = OrderBookAnalyzer()
    result = analyzer.analyze(bid_volume=700.0, ask_volume=300.0)
    assert result["imbalance"] > 0.0
    assert result["pressure"] == "BUYING_PRESSURE"


def test_tradeflow_analyzer_detects_delta():
    flow = TradeFlowAnalyzer()
    delta = flow.aggregate_delta(buy_volume=150.0, sell_volume=90.0)
    assert delta > 0.0


def test_backtest_engine_runs_simple_strategy():
    engine = BacktestEngine()
    closes = [100.0, 100.5, 101.0, 101.3, 101.4, 101.2]
    result = engine.run(closes, fee_rate=0.0005, slippage=0.0003)
    assert result["n_trades"] >= 0
    assert "total_return" in result
    assert "final_equity" in result

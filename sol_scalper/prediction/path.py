from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PredictionPathPoint:
    minute: int
    price: float
    probability: float


@dataclass
class PredictionPath:
    direction: str
    expected_return: float
    points: list[PredictionPathPoint]
    upper_band: float
    lower_band: float


class PathPredictor:
    """Build a simple projected 5–10 minute price path with confidence bands."""

    def predict(self, current_price: float, base_return: float, direction: str, horizon_minutes: int = 5) -> PredictionPath:
        if direction == "LONG":
            drift = max(base_return, 0.0005)
        elif direction == "SHORT":
            drift = -max(base_return, 0.0005)
        else:
            drift = 0.0

        points: list[PredictionPathPoint] = []
        price = float(current_price)
        for minute in range(1, horizon_minutes + 1):
            step = drift * (minute / horizon_minutes)
            price = float(current_price * (1 + step))
            prob = 0.62 if direction == "LONG" else 0.58
            points.append(PredictionPathPoint(minute=minute, price=price, probability=prob))

        expected_return = drift
        upper_band = current_price * (1 + max(abs(expected_return), 0.003))
        lower_band = current_price * (1 - max(abs(expected_return), 0.003))
        return PredictionPath(direction=direction, expected_return=expected_return, points=points, upper_band=upper_band, lower_band=lower_band)

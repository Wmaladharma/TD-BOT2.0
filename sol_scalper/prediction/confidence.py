from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CalibratedProbability:
    long: float
    short: float
    neutral: float

    def normalized(self) -> tuple[float, float, float]:
        total = self.long + self.short + self.neutral
        if total == 0:
            return (0.0, 0.0, 0.0)
        return (self.long / total, self.short / total, self.neutral / total)


class ProbabilityCalibrator:
    """A simple probability calibrator that keeps outputs grounded and conservative."""

    def __init__(self, model_score: float, confidence_bias: float = 0.10) -> None:
        self.model_score = model_score
        self.confidence_bias = confidence_bias

    def calibrate(self) -> CalibratedProbability:
        score = max(0.0, min(1.0, self.model_score))
        long_p = max(0.0, min(1.0, score + self.confidence_bias))
        short_p = max(0.0, min(1.0, (1.0 - score) * 0.65))
        neutral_p = max(0.0, 1.0 - long_p)
        remaining = max(0.0, 1.0 - long_p - short_p)
        if remaining > 0:
            neutral_p = remaining
        else:
            neutral_p = max(0.0, 1.0 - long_p - short_p)
            short_p = max(0.0, 1.0 - long_p - neutral_p)

        total = long_p + short_p + neutral_p
        if total == 0:
            return CalibratedProbability(long=0.0, short=0.0, neutral=0.0)
        return CalibratedProbability(
            long=long_p / total,
            short=short_p / total,
            neutral=neutral_p / total,
        )

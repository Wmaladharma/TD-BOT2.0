from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.linear_model import LogisticRegression


@dataclass
class ModelPrediction:
    direction: str
    probability: float
    expected_return: float


class DirectionalModel:
    """Tiny, interpretable baseline classifier for direction scoring."""

    def __init__(self) -> None:
        self.model = LogisticRegression(max_iter=500, random_state=42)
        self._trained = False

    def fit(self, X, y) -> None:
        labels = set(y)
        if len(labels) < 2:
            raise ValueError("DirectionalModel requires at least two target classes for training")
        self.model.fit(X, y)
        self._trained = True

    def predict_proba(self, X):
        if not self._trained:
            raise ValueError("Model must be fit before prediction")
        X_arr = np.asarray(X, dtype=float)
        if X_arr.ndim == 1:
            X_arr = X_arr.reshape(1, -1)
        return self.model.predict_proba(X_arr)

    def predict(self, X, expected_return: float = 0.0) -> ModelPrediction:
        if not self._trained:
            raise ValueError("Model must be fit before prediction")
        probs = self.predict_proba(X)[0]
        idx = int(probs.argmax())
        classes = ["DOWN", "UP"]
        direction = classes[idx]
        probability = float(probs[idx])
        return ModelPrediction(direction=direction, probability=probability, expected_return=expected_return)

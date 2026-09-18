from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier


class SeverityModel:

    FEATURE_NAMES = [
        "alert_count",
        "high_severity_alerts",
        "critical_severity_alerts",
        "error_alerts",
        "timeout_alerts",
        "connection_alerts",
        "resource_alerts",
        "log_count",
        "dependency_count",
        "recent_change_count",
        "has_metrics",
        "has_system_state",
    ]

    def __init__(self):
        self.model = GradientBoostingClassifier(
            random_state=42
        )
        self.is_trained = False

    def train(
        self,
        training_features: list[dict],
        labels: list[str],
    ) -> None:

        X = self._prepare_features(training_features)

        self.model.fit(X, labels)
        self.is_trained = True

    def predict(self, features: dict) -> dict:

        if not self.is_trained:
            raise RuntimeError(
                "Severity model must be trained before prediction"
            )

        X = self._prepare_features([features])

        prediction = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]

        confidence = float(np.max(probabilities))

        return {
            "severity": str(prediction),
            "confidence": round(confidence, 3),
        }

    def save(self, path: str) -> None:

        if not self.is_trained:
            raise RuntimeError(
                "Cannot save an untrained severity model"
            )

        Path(path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        joblib.dump(self.model, path)

    def load(self, path: str) -> None:

        self.model = joblib.load(path)
        self.is_trained = True

    def _prepare_features(
        self,
        features_list: list[dict]
    ) -> np.ndarray:

        return np.array(
            [
                [
                    float(features.get(name, 0))
                    for name in self.FEATURE_NAMES
                ]
                for features in features_list
            ]
        )
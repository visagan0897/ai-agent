from pathlib import Path

import numpy as np
import onnxruntime as ort


class ONNXSeverityInference:

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

    def __init__(self, model_path: str):
        path = Path(model_path)

        if not path.exists():
            raise FileNotFoundError(
                f"ONNX model not found: {path}"
            )

        self.session = ort.InferenceSession(
            str(path),
            providers=["CPUExecutionProvider"],
        )

        self.input_name = self.session.get_inputs()[0].name

    def predict(self, features: dict) -> dict:
        values = [
            float(features.get(name, 0))
            for name in self.FEATURE_NAMES
        ]

        input_data = np.array(
            [values],
            dtype=np.float32,
        )

        outputs = self.session.run(
            None,
            {
                self.input_name: input_data,
            },
        )

        labels = outputs[0]
        probabilities = outputs[1]

        severity = str(labels[0])

        probability_map = probabilities[0]

        confidence = float(
            max(
                probability_map.values()
            )
        )

        return {
            "severity": severity,
            "confidence": round(confidence, 3),
        }
from pathlib import Path

import joblib
import numpy as np
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType


MODEL_PATH = Path("prioritization/model/severity_model.joblib")
ONNX_PATH = Path("prioritization/model/severity_model.onnx")


def export_model() -> None:
    model = joblib.load(MODEL_PATH)

    feature_count = len(model.feature_importances_)

    initial_type = [
        (
            "float_input",
            FloatTensorType([None, feature_count]),
        )
    ]

    onnx_model = convert_sklearn(
        model,
        initial_types=initial_type,
        target_opset=17,
    )

    ONNX_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    ONNX_PATH.write_bytes(
        onnx_model.SerializeToString()
    )

    print("ONNX model exported successfully.")
    print(f"Model saved to: {ONNX_PATH}")


if __name__ == "__main__":
    export_model()
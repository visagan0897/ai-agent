from pathlib import Path

from prioritization.severity_model import SeverityModel
from prioritization.training_data import (
    TRAINING_FEATURES,
    TRAINING_LABELS,
)


MODEL_PATH = Path("prioritization/model/severity_model.joblib")


def train_model() -> None:
    model = SeverityModel()

    model.train(
        training_features=TRAINING_FEATURES,
        labels=TRAINING_LABELS,
    )

    model.save(str(MODEL_PATH))

    print(f"Model trained successfully.")
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()
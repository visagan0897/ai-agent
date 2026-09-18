from datetime import datetime
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer

from models.alerts import NormalizedAlert


class AlertClusterer:
    """
    Context-aware alert correlation.

    Correlation considers:
    - Message similarity
    - Same service
    - Same source
    - Same alert type
    - Time proximity
    """

    def cluster(
        self,
        alerts: list[NormalizedAlert],
        eps: float = 0.5,
        min_samples: int = 2,
    ) -> dict[int, list[NormalizedAlert]]:

        if not alerts:
            return {}

        # ---------------------------------------------------------
        # 1. Text similarity
        # ---------------------------------------------------------
        texts = [alert.normalized_message for alert in alerts]

        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(texts)

        text_similarity = (vectors @ vectors.T).toarray()

        # ---------------------------------------------------------
        # 2. Build contextual similarity matrix
        # ---------------------------------------------------------
        similarity_matrix = np.zeros((len(alerts), len(alerts)))

        for i in range(len(alerts)):
            for j in range(len(alerts)):

                if i == j:
                    similarity_matrix[i][j] = 1.0
                    continue

                alert_a = alerts[i]
                alert_b = alerts[j]

                score = 0.0

                # Message similarity
                score += 0.35 * text_similarity[i][j]

                # Same service
                if alert_a.service == alert_b.service:
                    score += 0.35

                # Same source
                if alert_a.source == alert_b.source:
                    score += 0.10

                # Same alert type
                if (
                    alert_a.alert_type
                    and alert_b.alert_type
                    and alert_a.alert_type == alert_b.alert_type
                ):
                    score += 0.05

                # Time proximity
                time_score = self._time_proximity(
                    alert_a.timestamp,
                    alert_b.timestamp,
                )

                score += 0.15 * time_score

                similarity_matrix[i][j] = min(score, 1.0)

        # ---------------------------------------------------------
        # 3. Convert similarity → distance
        # ---------------------------------------------------------
        distance_matrix = 1.0 - similarity_matrix

        # Numerical safety
        distance_matrix = np.clip(distance_matrix, 0.0, 1.0)

        # ---------------------------------------------------------
        # 4. DBSCAN clustering
        # ---------------------------------------------------------
        model = DBSCAN(
            eps=eps,
            min_samples=min_samples,
            metric="precomputed",
        )

        labels = model.fit_predict(distance_matrix)

        # ---------------------------------------------------------
        # 5. Build cluster dictionary
        # ---------------------------------------------------------
        clusters: dict[int, list[NormalizedAlert]] = {}

        for alert, label in zip(alerts, labels):
            clusters.setdefault(int(label), []).append(alert)

        return clusters

    def _time_proximity(
        self,
        timestamp_a: datetime,
        timestamp_b: datetime,
    ) -> float:

        difference = abs(
            (timestamp_a - timestamp_b).total_seconds()
        )

        # Same moment → strongest relationship
        if difference <= 60:
            return 1.0

        # Within 5 minutes → strong relationship
        if difference <= 300:
            return 0.8

        # Within 15 minutes → moderate relationship
        if difference <= 900:
            return 0.5

        # Within 30 minutes → weak relationship
        if difference <= 1800:
            return 0.2

        return 0.0
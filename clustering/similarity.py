from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from models.alerts import NormalizedAlert


class AlertSimilarity:

    def build_similarity_matrix(
        self,
        alerts: list[NormalizedAlert]
    ):
        if not alerts:
            return []

        texts = [
            alert.normalized_message
            for alert in alerts
        ]

        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(texts)

        return cosine_similarity(vectors)

    def find_near_matches(
        self,
        alerts: list[NormalizedAlert],
        threshold: float = 0.5
    ) -> list[tuple[str, str, float]]:

        if len(alerts) < 2:
            return []

        matrix = self.build_similarity_matrix(alerts)
        matches = []

        for i in range(len(alerts)):
            for j in range(i + 1, len(alerts)):

                score = round(float(matrix[i][j]), 3)

                if score >= threshold:
                    matches.append(
                        (
                            alerts[i].alert_id,
                            alerts[j].alert_id,
                            score,
                        )
                    )

        return matches
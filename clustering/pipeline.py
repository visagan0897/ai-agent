from models.alerts import NormalizedAlert

from clustering.similarity import AlertSimilarity
from clustering.dbscan_cluster import AlertClusterer
from clustering.outlier import OutlierDetector
from clustering.incident_builder import IncidentBuilder


class CorrelationPipeline:

    def __init__(self):
        self.similarity = AlertSimilarity()
        self.clusterer = AlertClusterer()
        self.outlier_detector = OutlierDetector()
        self.incident_builder = IncidentBuilder()

    def process(
        self,
        alerts: list[NormalizedAlert],
        evidence: dict | None = None,
    ) -> dict:

        if not alerts:
            return {
                "incidents": [],
                "outliers": [],
            }

        evidence = evidence or {}

        clusters = self.clusterer.cluster(alerts)

        normal_clusters, outliers = (
            self.outlier_detector.separate(clusters)
        )

        incidents = []

        for cluster_id, cluster_alerts in normal_clusters.items():

            incident = self.incident_builder.build(
                cluster_id,
                cluster_alerts,
                logs=evidence.get("logs", {}).get("logs", []),
                metrics=evidence.get("metrics", {}).get("metrics", {}),
                recent_changes=evidence.get(
                    "recent_changes",
                    []
                ),
                dependencies=evidence.get(
                    "dependencies",
                    []
                ),
                system_state=evidence.get(
                    "system_state",
                    {}
                ),
            )

            incidents.append(incident)

        return {
            "incidents": incidents,
            "outliers": outliers,
        }
from models.alerts import NormalizedAlert


class OutlierDetector:

    def separate(
        self,
        clusters: dict[int, list[NormalizedAlert]]
    ) -> tuple[dict[int, list[NormalizedAlert]], list[NormalizedAlert]]:

        normal_clusters: dict[int, list[NormalizedAlert]] = {}
        outliers: list[NormalizedAlert] = []

        for cluster_id, alerts in clusters.items():

            if cluster_id == -1:
                outliers.extend(alerts)
            else:
                normal_clusters[cluster_id] = alerts

        return normal_clusters, outliers
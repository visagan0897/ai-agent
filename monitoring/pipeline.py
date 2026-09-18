from models.alerts import Alert, NormalizedAlert

from preprocessing.parser import AlertParser
from preprocessing.normalizer import AlertNormalizer
from preprocessing.deduplicator import AlertDeduplicator


class MonitoringPipeline:

    def __init__(self):
        self.parser = AlertParser()
        self.normalizer = AlertNormalizer()
        self.deduplicator = AlertDeduplicator()

    def process(
        self,
        alerts: list[Alert],
    ) -> list[NormalizedAlert]:

        normalized_alerts = []

        for alert in alerts:
            parsed_alert = self.parser.parse(
                alert.model_dump()
            )

            normalized_alerts.append(
                self.normalizer.normalize(
                    parsed_alert
                )
            )

        return self.deduplicator.deduplicate(
            normalized_alerts
        )
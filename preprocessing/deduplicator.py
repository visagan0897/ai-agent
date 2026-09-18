from models.alerts import NormalizedAlert


class AlertDeduplicator:

    def deduplicate(
        self,
        alerts: list[NormalizedAlert]
    ) -> list[NormalizedAlert]:

        unique_alerts = []
        seen = set()

        for alert in alerts:
            fingerprint = self._create_fingerprint(alert)

            if fingerprint in seen:
                continue

            seen.add(fingerprint)
            unique_alerts.append(alert)

        return unique_alerts

    def _create_fingerprint(self, alert: NormalizedAlert) -> tuple:
        return (
            alert.service,
            alert.source,
            alert.normalized_message,
            alert.alert_type,
        )
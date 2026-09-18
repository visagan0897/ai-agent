from datetime import datetime

from models.alerts import NormalizedAlert
from models.incidents import Incident


class IncidentBuilder:

    def build(
        self,
        cluster_id: int,
        alerts: list[NormalizedAlert],
        logs: list[str] | None = None,
        metrics: dict | None = None,
        recent_changes: list[str] | None = None,
        dependencies: list[str] | None = None,
        system_state: dict | None = None,
    ) -> Incident:

        if not alerts:
            raise ValueError(
                "Cannot build an incident from an empty alert list"
            )

        services = sorted(
            {alert.service for alert in alerts}
        )

        description = self._build_description(alerts)

        return Incident(
            incident_id=f"INC-{cluster_id}",
            created_at=datetime.now(),
            service=", ".join(services),
            description=description,
            alerts=alerts,
            logs=logs or [],
            metrics=metrics or {},
            recent_changes=recent_changes or [],
            dependencies=dependencies or [],
            system_state=system_state or {},
            cluster_id=str(cluster_id),
        )

    def _build_description(
        self,
        alerts: list[NormalizedAlert],
    ) -> str:

        alert_types = sorted(
            {
                alert.alert_type
                for alert in alerts
                if alert.alert_type
            }
        )

        if alert_types:
            return (
                f"Incident involving {len(alerts)} related alerts "
                f"with symptoms: {', '.join(alert_types)}."
            )

        return (
            f"Incident involving {len(alerts)} related alerts."
        )
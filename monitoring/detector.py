from datetime import datetime
from typing import Any

from models.alerts import Alert


class IncidentDetector:

    def detect(
        self,
        health: dict[str, Any],
        logs: dict[str, Any],
        metrics: dict[str, Any],
    ) -> list[Alert]:

        alerts: list[Alert] = []

        service = health.get("service", "unknown")
        timestamp = datetime.now()

        # Detect unhealthy service
        if health.get("status") == "unhealthy":
            alerts.append(
                Alert(
                    alert_id=f"HEALTH-{service}-{timestamp.timestamp()}",
                    timestamp=timestamp,
                    source="health-monitor",
                    service=service,
                    message=f"{service} is unhealthy",
                    severity="high",
                    metadata={
                        "status_code": health.get("status_code"),
                        "error": health.get("error"),
                    },
                )
            )

        # Detect log-based failures
        for index, log in enumerate(logs.get("logs", [])):
            message = str(log)

            alerts.append(
                Alert(
                    alert_id=f"LOG-{service}-{index}-{timestamp.timestamp()}",
                    timestamp=timestamp,
                    source="log-monitor",
                    service=service,
                    message=message,
                    metadata={},
                )
            )

        # Detect metric anomalies
        metric_values = metrics.get("metrics", {})

        for metric_name, value in metric_values.items():
            if isinstance(value, (int, float)) and value > 0:
                alerts.append(
                    Alert(
                        alert_id=(
                            f"METRIC-{service}-"
                            f"{metric_name}-{timestamp.timestamp()}"
                        ),
                        timestamp=timestamp,
                        source="metrics-monitor",
                        service=service,
                        message=f"{metric_name} reported value {value}",
                        metadata={
                            "metric": metric_name,
                            "value": value,
                        },
                    )
                )

        return alerts
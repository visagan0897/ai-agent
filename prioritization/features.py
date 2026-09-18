from models.incidents import Incident


class IncidentFeatureExtractor:

    def extract(self, incident: Incident) -> dict:
        alerts = incident.alerts

        return {
            "alert_count": len(alerts),
            "high_severity_alerts": self._count_severity(alerts, "high"),
            "critical_severity_alerts": self._count_severity(alerts, "critical"),
            "error_alerts": self._count_alert_type(alerts, "error"),
            "timeout_alerts": self._count_alert_type(alerts, "timeout"),
            "connection_alerts": self._count_alert_type(alerts, "connection"),
            "resource_alerts": self._count_alert_type(alerts, "resource"),
            "log_count": len(incident.logs),
            "dependency_count": len(incident.dependencies),
            "recent_change_count": len(incident.recent_changes),
            "has_metrics": int(bool(incident.metrics)),
            "has_system_state": int(bool(incident.system_state)),
        }

    def _count_severity(self, alerts, severity: str) -> int:
        return sum(
            1
            for alert in alerts
            if alert.severity == severity
        )

    def _count_alert_type(self, alerts, alert_type: str) -> int:
        return sum(
            1
            for alert in alerts
            if alert.alert_type == alert_type
        )
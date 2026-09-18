from models.incidents import Incident


class IncidentInvestigator:

    def build_evidence_context(self, incident: Incident) -> dict:
        return {
            "incident_id": incident.incident_id,
            "service": incident.service,
            "description": incident.description,
            "alerts": [
                {
                    "alert_id": alert.alert_id,
                    "service": alert.service,
                    "message": alert.original_message,
                    "normalized_message": alert.normalized_message,
                    "alert_type": alert.alert_type,
                    "severity": alert.severity,
                    "source": alert.source,
                }
                for alert in incident.alerts
            ],
            "logs": incident.logs,
            "metrics": incident.metrics,
            "recent_changes": incident.recent_changes,
            "dependencies": incident.dependencies,
            "system_state": incident.system_state,
        }
from models import IncidentRequest


class IncidentAgent:

    def analyze(self, incident: IncidentRequest):
        return {
            "incident_id": incident.incident_id,
            "status": "analysis_pending"
        }
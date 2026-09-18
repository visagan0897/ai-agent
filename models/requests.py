from pydantic import BaseModel


class IncidentRequest(BaseModel):
    incident_id: str
    service: str
    description: str
    alerts: list[str]
    logs: list[str]
    metrics: dict
    recent_changes: list[str]
    dependencies: list[str]
    system_state: dict
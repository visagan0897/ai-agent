from datetime import datetime

from pydantic import BaseModel, Field

from models.alerts import NormalizedAlert


class Incident(BaseModel):
    incident_id: str
    created_at: datetime
    service: str
    description: str

    alerts: list[NormalizedAlert] = Field(default_factory=list)

    logs: list[str] = Field(default_factory=list)
    metrics: dict = Field(default_factory=dict)
    recent_changes: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    system_state: dict = Field(default_factory=dict)

    cluster_id: str | None = None
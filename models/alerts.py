from datetime import datetime

from pydantic import BaseModel, Field


class Alert(BaseModel):
    alert_id: str
    timestamp: datetime
    source: str
    service: str
    message: str
    severity: str | None = None
    metadata: dict = Field(default_factory=dict)


class NormalizedAlert(BaseModel):
    alert_id: str
    timestamp: datetime
    source: str
    service: str
    original_message: str
    normalized_message: str
    alert_type: str | None = None
    severity: str | None = None
    metadata: dict = Field(default_factory=dict)
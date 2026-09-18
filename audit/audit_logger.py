from datetime import datetime
from pathlib import Path
import json
from typing import Any


class AuditLogger:

    def __init__(self, log_path: str = "audit/audit_log.jsonl"):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def log(
        self,
        event_type: str,
        incident_id: str,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        record = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "incident_id": incident_id,
            "data": data or {},
        }

        with self.log_path.open(
            "a",
            encoding="utf-8",
        ) as file:
            file.write(
                json.dumps(record, default=str)
                + "\n"
            )

        return record
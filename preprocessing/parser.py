import re

from models.alerts import Alert


class AlertParser:

    def parse(self, raw_alert: dict) -> Alert:
        return Alert(
            alert_id=str(raw_alert.get("alert_id", "")),
            timestamp=raw_alert["timestamp"],
            source=str(raw_alert.get("source", "unknown")),
            service=str(raw_alert.get("service", "unknown")),
            message=self._clean_message(raw_alert.get("message", "")),
            severity=self._extract_severity(raw_alert),
            metadata=raw_alert.get("metadata", {}),
        )

    def _clean_message(self, message: str) -> str:
        message = str(message).strip()
        message = re.sub(r"\s+", " ", message)
        return message

    def _extract_severity(self, raw_alert: dict) -> str | None:
        severity = raw_alert.get("severity")

        if severity is None:
            return None

        return str(severity).lower().strip()
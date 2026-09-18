import re

from models.alerts import Alert, NormalizedAlert


class AlertNormalizer:

    def normalize(self, alert: Alert) -> NormalizedAlert:
        normalized_message = self._normalize_message(alert.message)

        return NormalizedAlert(
            alert_id=alert.alert_id,
            timestamp=alert.timestamp,
            source=alert.source,
            service=alert.service,
            original_message=alert.message,
            normalized_message=normalized_message,
            alert_type=self._detect_alert_type(normalized_message),
            severity=alert.severity,
            metadata=alert.metadata,
        )

    def _normalize_message(self, message: str) -> str:
        message = message.lower().strip()

        # Normalize numbers
        message = re.sub(r"\b\d+(?:\.\d+)?\b", "<number>", message)

        # Normalize whitespace
        message = re.sub(r"\s+", " ", message)

        return message

    def _detect_alert_type(self, message: str) -> str | None:
        if "timeout" in message:
            return "timeout"

        if "connection" in message:
            return "connection"

        if "error" in message or "failed" in message:
            return "error"

        if "latency" in message:
            return "latency"

        if "cpu" in message:
            return "resource"

        if "memory" in message:
            return "resource"

        return None
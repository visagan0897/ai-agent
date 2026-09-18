from typing import Any

from monitoring.health_monitor import HealthMonitor


class IncidentVerifier:

    def __init__(self):
        self.health_monitor = HealthMonitor()

    async def verify(
        self,
        service: str,
        url: str,
    ) -> dict[str, Any]:

        health = await self.health_monitor.check(
            service,
            url,
        )

        status = str(
            health.get("status", "unknown")
        ).lower()

        if status in {
            "unhealthy",
            "down",
            "failed",
            "degraded",
        }:
            return {
                "status": "failed",
                "recovered": False,
                "service": service,
                "reason": (
                    "The service is still reporting "
                    "an unhealthy state."
                ),
                "health": health,
            }

        if status == "healthy":
            return {
                "status": "recovered",
                "recovered": True,
                "service": service,
                "reason": (
                    "The service is reporting "
                    "a healthy state after remediation."
                ),
                "health": health,
            }

        return {
            "status": "unknown",
            "recovered": False,
            "service": service,
            "reason": (
                "The service returned an unknown "
                "health state."
            ),
            "health": health,
        }
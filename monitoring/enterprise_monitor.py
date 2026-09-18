import httpx

from monitoring.health_monitor import HealthMonitor
from monitoring.log_monitor import LogMonitor
from monitoring.metrics_monitor import MetricsMonitor


class EnterpriseMonitor:

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

        self.health_monitor = HealthMonitor()
        self.log_monitor = LogMonitor()
        self.metrics_monitor = MetricsMonitor()

    async def collect(self, service: str) -> dict:

        health = await self.health_monitor.check(
            service,
            f"{self.base_url}/health",
        )

        logs = await self.log_monitor.collect(
            service,
            f"{self.base_url}/logs",
        )

        metrics = await self.metrics_monitor.collect(
            service,
            f"{self.base_url}/metrics",
        )

        # Remove simulator-internal cause information.
        # The AI should reason from observable evidence only.
        health.pop("failure", None)
        health.pop("scenario", None)

        return {
            "health": health,
            "logs": logs,
            "metrics": metrics,
        }
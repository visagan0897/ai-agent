from models.incidents import Incident


class BusinessImpactAnalyzer:

    def analyze(self, incident: Incident) -> dict:
        affected_services = self._affected_services(incident)
        dependency_count = len(incident.dependencies)

        return {
            "affected_services": affected_services,
            "affected_service_count": len(affected_services),
            "dependency_count": dependency_count,
            "has_customer_facing_service": self._has_customer_facing_service(
                incident
            ),
            "impact_evidence": self._collect_impact_evidence(incident),
        }

    def _affected_services(self, incident: Incident) -> list[str]:
        services = {
            alert.service
            for alert in incident.alerts
            if alert.service
        }

        if incident.service:
            services.update(
                service.strip()
                for service in incident.service.split(",")
                if service.strip()
            )

        return sorted(services)

    def _has_customer_facing_service(
        self,
        incident: Incident,
    ) -> bool:
        customer_facing = {
            "api-gateway",
            "order-service",
            "payment-service",
            "inventory-service",
        }

        affected = set(self._affected_services(incident))

        return bool(affected & customer_facing)

    def _collect_impact_evidence(
        self,
        incident: Incident,
    ) -> list[str]:
        evidence = []

        if incident.logs:
            evidence.append(
                f"{len(incident.logs)} related log entries available"
            )

        if incident.metrics:
            evidence.append(
                "Operational metrics are available"
            )

        if incident.system_state:
            evidence.append(
                "Current system-state information is available"
            )

        if incident.dependencies:
            evidence.append(
                f"{len(incident.dependencies)} dependencies are affected or relevant"
            )

        return evidence
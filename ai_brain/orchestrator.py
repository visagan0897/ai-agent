from ai_brain.decision_engine import AIDecisionEngine
from models.incidents import Incident
from prioritization.prioritizer import IncidentPrioritizer
from remediation.action_planner import ActionPlanner


class IncidentOrchestrator:

    def __init__(
        self,
        severity_model_path: str,
    ):
        self.prioritizer = IncidentPrioritizer(
            severity_model_path
        )
        self.decision_engine = AIDecisionEngine()
        self.action_planner = ActionPlanner()

    async def process(
        self,
        incident: Incident,
    ) -> dict:

        # Step 1: Determine incident priority
        priority = self.prioritizer.prioritize(
            incident
        )

        # Step 2: AI investigates and makes a decision
        ai_decision = await self.decision_engine.decide(
            incident
        )

        # Step 3: Convert AI decision into an executable request
        action_request = self.action_planner.plan(
            ai_decision
        )

        return {
            "incident_id": incident.incident_id,
            "priority": priority,
            "ai_decision": ai_decision,
            "action_request": action_request,
        }
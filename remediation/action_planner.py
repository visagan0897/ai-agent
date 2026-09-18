from typing import Any


class ActionPlanner:

    def plan(
        self,
        ai_decision: dict[str, Any],
    ) -> dict[str, Any]:

        selected_action = ai_decision.get("selected_action")

        if not isinstance(selected_action, dict):
            raise ValueError(
                "AI decision does not contain a valid selected_action"
            )

        action_id = selected_action.get("action_id")
        action = selected_action.get("action")
        reason = selected_action.get("reason")

        if not action_id:
            raise ValueError(
                "AI decision does not contain an action_id"
            )

        if not action:
            raise ValueError(
                "AI decision does not contain an action"
            )

        return {
            "incident_id": ai_decision.get("incident_id"),
            "action_id": action_id,
            "requested_action": action_id,
            "action": action,
            "reason": reason,
            "execution_mode": ai_decision.get(
                "execution_mode",
                "human_approval",
            ),
        }
from typing import Any
import inspect

from remediation.action_registry import ActionRegistry


class RemediationExecutor:

    def __init__(self, registry: ActionRegistry):
        self.registry = registry

    async def execute(
        self,
        action_request: dict[str, Any],
    ) -> dict[str, Any]:

        action = action_request.get("requested_action")

        execution_mode = action_request.get(
            "execution_mode",
            "human_approval",
        )

        if not action:
            raise ValueError("No action requested")

        if execution_mode == "human_approval":
            return {
                "status": "pending_approval",
                "action": action,
                "message": "Human approval is required before execution.",
            }

        if execution_mode != "autonomous":
            raise ValueError(
                f"Invalid execution mode: {execution_mode}"
            )

        if not self.registry.is_allowed(action):
            return {
                "status": "blocked",
                "action": action,
                "message": "Action is not registered for execution.",
            }

        handler = self.registry.get(action)

        result = handler()

        if inspect.isawaitable(result):
            result = await result

        return {
            "status": "executed",
            "action": action,
            "result": result,
        }
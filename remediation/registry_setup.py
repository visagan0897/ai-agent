from remediation.action_registry import ActionRegistry
from remediation.payment_actions import recover_payment_service


def create_action_registry() -> ActionRegistry:
    registry = ActionRegistry()

    registry.register(
        "recover_payment_service",
        recover_payment_service,
    )

    return registry
from typing import Callable, Any


class ActionRegistry:

    def __init__(self):
        self._actions: dict[str, Callable[..., Any]] = {}

    def register(
        self,
        name: str,
        handler: Callable[..., Any],
    ) -> None:

        if not name:
            raise ValueError("Action name cannot be empty")

        if not callable(handler):
            raise TypeError("Action handler must be callable")

        self._actions[name] = handler

    def is_allowed(self, name: str) -> bool:
        return name in self._actions

    def get(self, name: str) -> Callable[..., Any]:
        if name not in self._actions:
            raise ValueError(
                f"Action is not registered: {name}"
            )

        return self._actions[name]

    def list_actions(self) -> list[str]:
        return sorted(self._actions.keys())
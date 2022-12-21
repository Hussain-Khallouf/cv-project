from typing import List, Tuple


class ActionsRepo:
    _actions: List[Tuple[str, dict]]
    _retreated_actions: List[Tuple[str, dict]]

    def __init__(self):
        self._actions = []
        self._retreated_actions = []

    def push(self, action: str, kwargs: dict):
        self._actions.append((action, kwargs))

    def pop(self) -> Tuple[str, dict]:
        return self._actions.pop()

    def undo(self):
        self._retreated_actions.append(self._actions.pop()) if len(
            self._actions
        ) else None

    def redo(self):
        self._actions.append(self._retreated_actions.pop()) if len(
            self._retreated_actions
        ) else None

    def get_actions(self) -> List[Tuple[str, dict]]:
        return self._actions

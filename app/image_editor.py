"""
handle usacase, repo
"""
from typing import Tuple, List
from numpy._typing import NDArray
from app.repo.image_repo import Image
from app.usecases.editor_usesaces import EditorUS
from app.config.config import Actions


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


class ImageEditor:
    def __init__(self, editor_uc: EditorUS) -> None:
        self._original_image = Image()
        self._edited_image = Image()
        self._editor_uc = editor_uc
        self._actions_repo: ActionsRepo = None
        self.is_actions_applied = True
        self.actions2func = self.get_actions2func_dict(
            editor_uc
        )  # self.actions2func["action"](**kwargs)

    def get_actions2func_dict(self, editor_uc):
        return {Actions.blurring.value: editor_uc.blur}

    def set_image(self, image: NDArray):
        self._original_image.set_image(image)
        self._actions_repo = ActionsRepo()

    def undo(self) -> NDArray:
        self._actions_repo.undo()

    def redo(self) -> NDArray:
        self._actions_repo.redo()

    def blurring(self) -> NDArray:
        self._actions_repo.push(Actions.blurring.value, {})

    def _apply_actions(self, image: NDArray):
        edited_image = image
        for action, kwargs in self._actions_repo.get_actions():
            edited_image = self.actions2func.get(
                action, lambda: print("Not Found Action")
            )(image=edited_image, **kwargs)
        return edited_image

    def get_edited_image(self):
        # TODO: add is_actions_applied flag for better performance
        # if not self.is_actions_applied:
        # image = self.original_image.get_image()
        # new_edited_image = self._apply_actions(image)
        # self._edited_image.set_image(new_edited_image)
        # self.is_actions_applied = True
        return self._apply_actions(self._original_image.get_image())

"""
handle usacase, repo
"""
from typing import Tuple, List
from numpy._typing import NDArray
from app.repo.image_repo import Image
from app.usecases.editor_usesaces import EditorUS
from app.config.config import Actions
from app.repo.action_repo import ActionsRepo


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
        return {
            Actions.BLURRING.value: editor_uc.blur,
            Actions.TRANSLATE.value: editor_uc.translate,
        }

    def set_image(self, image: NDArray):
        self._original_image.set_image(image)
        self._actions_repo = ActionsRepo()

    def undo(self):
        self._actions_repo.undo()

    def redo(self):
        self._actions_repo.redo()

    def blurring(self):
        self._actions_repo.push(Actions.BLURRING.value, {})

    def translate(self):
        self._actions_repo.push(Actions.TRANSLATE.value, {})

    def rotate(self):
        self._actions_repo.push(Actions.ROATTE.value, {})

    def _apply_actions(self, image: NDArray):
        edited_image = image
        for action, kwargs in self._actions_repo.get_actions():
            edited_image = self.actions2func.get(
                action, lambda: print("Not Found Action")
            )(image=edited_image, **kwargs)
        return edited_image

    def get_edited_image(self):
        # TODO: add is_actions_applied flag for better performance For hussain
        # if not self.is_actions_applied:
        # image = self.original_image.get_image()
        # new_edited_image = self._apply_actions(image)
        # self._edited_image.set_image(new_edited_image)
        # self.is_actions_applied = True
        return self._apply_actions(self._original_image.get_image())

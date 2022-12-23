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
        self.is_actions_applied = False
        self.actions2func = self.get_actions2func_dict()

    def get_actions2func_dict(self):
        return {
            Actions.NO_ACTION.value: lambda image, kwargs: image,
            Actions.BLURRING.value: self.blurring,
            Actions.TRANSLATE_VERTICAL.value: self.translate_vertical,
            Actions.TRANSLATE_HORIZONTAL.value: self.translate_horizontal,
            Actions.SKEW.value: self.skew,
            Actions.SCALE.value: self.scale,
            Actions.ROTATE.value: self.rotate,
        }

    def set_image(self, image: NDArray):
        self._original_image.set_image(image)
        self._actions_repo = ActionsRepo()

    def undo(self):
        self._actions_repo.undo()

    def redo(self):
        self._actions_repo.redo()



    def blurring(self, image: NDArray, kwargs):
        return self._editor_uc.blur(image, **kwargs)

    def translate_vertical(self, image: NDArray, kwargs):
        return self._editor_uc.translate_vertical(image, **kwargs)

    def translate_horizontal(self, image: NDArray, kwargs):
        return self._editor_uc.translate_horizontal(image, **kwargs)

    def rotate(self, image: NDArray, kwargs):
        r = self._editor_uc.rotate(image, **kwargs)
        return r

    def scale(self, image: NDArray, kwargs):
        return self._editor_uc.scale(image, **kwargs)

    def skew(self, image: NDArray, kwargs):
        return self._editor_uc.skew(image, **kwargs)

    def add_action(self, action: Actions, kwargs):
        self._actions_repo.push(action.value, kwargs)
        self.is_actions_applied = False

    def _apply_actions(self, image: NDArray):
        edited_image = image
        for action, kwargs in self._actions_repo.get_actions():
            edited_image = self.actions2func.get(
                action, lambda: print("Not Found Action")
            )(image=edited_image, kwargs=kwargs)
        return edited_image

    def get_edited_image(self):
        if not self.is_actions_applied:
            image = self._original_image.get_image()
            new_edited_image = self._apply_actions(image)
            self._edited_image.set_image(new_edited_image)
            self.is_actions_applied = True
        return self._edited_image.get_image()

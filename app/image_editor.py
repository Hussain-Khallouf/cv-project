"""
handle usacase, repo
"""
from numpy._typing import NDArray
from app.repo.image_repo import ImageRepo
from app.usecases.editor_usesaces import EditorUS
from app.config.config import Actions


class ImageEditor:
    def __init__(self, image_repo: ImageRepo, editor_uc: EditorUS) -> None:
        self.image_ropo = image_repo
        self.editor_uc = editor_uc

    def set_image(self, image: NDArray) -> NDArray:
        self.image_ropo.push(image)
        return self.image_ropo.get_current_image()

    def undo(self) -> NDArray:
        self.image_ropo.go_backward()
        return self.image_ropo.get_current_image()

    def redo(self) -> NDArray:
        self.image_ropo.go_forward()
        return self.image_ropo.get_current_image()

    def blurring(self) -> NDArray:
        curr_image = self.image_ropo.get_current_image()
        blured = self.editor_uc.blur(curr_image)
        self.image_ropo.push(blured)
        return self.image_ropo.get_current_image()

    def _get_action_handler(self, action: Actions):
        action2handler = {
            Actions.blurring.value: self.blurring
        }

        return action2handler.get(action.value, None)

    def apply_action(self, action: Actions) -> NDArray:
        handler = self._get_action_handler(action)
        if not handler:
            raise ValueError("Incorrect Action")
        return handler()

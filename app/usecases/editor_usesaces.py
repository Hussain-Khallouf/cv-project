from typing import Tuple
from numpy._typing import NDArray
from app.controller.image_controller import ImageController


class EditorUS:
    def __init__(self, image_controller: ImageController) -> None:
        self.image_controller = image_controller

    def blur(self, image: NDArray, kernel_size: Tuple[int, int] = (3, 3)):
        if not image:
            raise ValueError("Image should not be null")
        return self.image_controller.blur(image, kernel_size)

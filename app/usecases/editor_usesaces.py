from typing import Tuple
from numpy._typing import NDArray
from app.controller.image_controller import ImageController


class EditorUS:
    def __init__(self, image_controller: ImageController) -> None:
        self.image_controller = image_controller

    def blur(self, image: NDArray, kernel_size: Tuple[int, int] = (3, 3)):
        if image is None:
            raise ValueError("Image should not be null")
        return self.image_controller.blur(image, kernel_size)

    def translate(self, image: NDArray, value: int = 10):
        return self.image_controller.translate(image, value, 0)

    def rotate(self, image: NDArray, value: int = 15):
        return self.image_controller.rotate(image, value)

    def scale(self, image: NDArray, value: int = 10):
        return self.image_controller.scale(image, value)

    def skew(self, image: NDArray, x: int = 0.5, y: int = 0):
        return self.image_controller.skew(image, x, y)

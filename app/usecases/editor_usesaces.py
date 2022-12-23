from typing import Tuple

import numpy as np
from numpy._typing import NDArray
from app.controller.image_controller import ImageController


class EditorUS:
    def __init__(self, image_controller: ImageController) -> None:
        self.image_controller = image_controller

    def blur(self, image: NDArray, kernel_size: Tuple[int, int] = (3, 3)):
        if image is None:
            raise ValueError("Image should not be null")
        return self.image_controller.blur(image, kernel_size)

    def translate_vertical(self, image: NDArray, value: int = 10):
        return np.roll(image, value, axis=0)

        # return self.image_controller.translate(image,0, value)

    def translate_horizontal(self, image: NDArray, value: int = 10):
        return np.roll(image, value, axis=1)
        # return self.image_controller.translate(image, value, 0)

    def rotate(self, image: NDArray, angle: int = 15):
        return self.image_controller.rotate(image, angle)

    def scale(self, image: NDArray, value: int = 10):
        return self.image_controller.scale(image, value)

    def skew(self, image: NDArray, x=0, y=0.5):
        return self.image_controller.skew(image, x, y)

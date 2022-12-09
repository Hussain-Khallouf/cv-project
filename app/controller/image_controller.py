"""
This module responsible for dealing with opencv
"""
import cv2 as cv
from typing import Tuple
from numpy._typing import NDArray


class ImageController:
    def blur(self, image: NDArray, kernel_size: Tuple[int, int]) -> NDArray:
        return cv.blur(image, kernel_size)

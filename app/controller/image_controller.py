"""
This module responsible for dealing with opencv
"""
import cv2 as cv
from typing import Tuple
from numpy._typing import NDArray
import numpy as np


class ImageController:
    def blur(self, image: NDArray, kernel_size: Tuple[int, int]) -> NDArray:
        return cv.blur(image, kernel_size)

    def translate(self, image: NDArray, x: int, y: int):
        M = np.float32([[1, 0, x], [0, 1, y]])
        shifted = cv.warpAffine(image, M, (image.shape[1], image.shape[0]))
        return shifted

    def rotate(self, image: NDArray, angle: int = 15):
        rotated = cv.rotate(image, angle)
        return rotated

    def scale(self, image: NDArray, value: int = 10):
        height, width, _ = image.shape
        dimension = (height + value, width + value)
        scaled = cv.resize(image, dimension, interpolation=cv.INTER_AREA)
        return scaled

    def skew(self, image: NDArray, x: float = 0.5, y: float = 0.0):
        """
        X & Y should be between 0  and 1
        """
        rows, cols, dim = image.shape
        M = np.float32([[1, x, 0], [y, 1, 0], [0, 0, 1]])
        sheared_img = cv.warpPerspective(
            image, M, (int(cols * (1 + x)), int(rows * (1 + y)))
        )
        return sheared_img

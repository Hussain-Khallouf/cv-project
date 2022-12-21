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

    def translate(self, image: NDArray, x: int, y: int ):
        M = np.float32([
            [1, 0, x],
            [0, 1, y]
        ])
        shifted = cv.warpAffine(image, M, (image.shape[1], image.shape[0]))
        return shifted



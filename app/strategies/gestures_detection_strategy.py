import cv2 as cv
import numpy as np
from numpy._typing import NDArray
from app.config import config
from gestures_detectors import GesturesDetectors
from haar import HaarCasCade
from back_projection import BackProjection
from helper import HelperCV


class GestureDetectionStrategy:

    def __init__(self):
        self.fingers = 0

    """
    abstract class for strategy design pattern
    you can implement gesture detection strategy as many as you want by inheriting from  this class
    """

    def detect(self, frame: NDArray) -> config.Gestures:
        pressed_key = cv.waitKey(1)
        backProjection = BackProjection(kernel_size=(7, 7))
        haarCasCade = HaarCasCade()
        gestures_detectors = GesturesDetectors()

        frame = cv.resize(frame, backProjection.size)
        mask_cascade = haarCasCade.apply(frame)
        thresh, view = backProjection.apply(frame, pressed_key)

        mask_cascade = cv.resize(mask_cascade, backProjection.size)

        frame = backProjection.draw_rectangle_for_detect_hist_skin(frame)
        thresh = cv.bitwise_and(mask_cascade, thresh)
        view = cv.bitwise_and(view, thresh)

        try:
            max_contour, convexhull, frame = HelperCV.draw_convex_hull(
                frame, thresh[:, :, 0])
            self.fingers = gestures_detectors.calculate_fingers(
                frame, convexhull, max_contour)
            frame = HelperCV.draw_text(frame, f"{self.fingers}")
        except Exception as e:
            print(e)

        return config.Gestures(self.fingers)

import cv2 as cv
import numpy as np
import math
from numpy._typing import NDArray
from app.config import config
from .face_haar_cascade import FaceHaarCasade
from app.utils import Colors
from app import utils
from app.strategies.gesture_detector import GesturesDetectors

face_path = ("haarcascade_frontalface_default.xml",)


class GestureDetectionStrategy:
    def __init__(self):
        self.fingers = 0
        self.i = 0
        self.face_cascade = FaceHaarCasade()
        self.gestures_detectors = GesturesDetectors()
        self.disc = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
        self.fgbg = cv.createBackgroundSubtractorMOG2(detectShadows=True)

    def _face_removal(self, image, thikness=10):
        image = self.face_cascade.remove_faces(image, thikness)
        return image

    def _hand_hist_mask(self, image, hand_hist):
        hsvt = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        dst = cv.calcBackProject([hsvt], [0, 1], hand_hist, [0, 180, 0, 256], 1)
        cv.filter2D(dst, -1, self.disc, dst)
        _, thresh = cv.threshold(dst, 50, 255, 0)
        # thresh = cv.merge((thresh, thresh, thresh))
        return thresh

    def detect(self, frame: NDArray, hand_hist) -> config.Gestures:
        # if self.i >= 30:
        #     self.fgbg = cv.createBackgroundSubtractorMOG2(detectShadows=True)
        #     self.i = 0

        # fmask = self.fgbg.apply(frame, learningRate=0)
        # fmask = cv.erode(fmask, np.ones((5, 5), np.uint8))
        removed_face_frame = self._face_removal(frame)
        mask = self._hand_hist_mask(removed_face_frame, hand_hist)
        # mask = cv.bitwise_and(frame, frame, mask=fmask)

        max_contour, convexhull, frame = utils.draw_convex_hull(frame, mask)
        frame, fingers = self.gestures_detectors.calculate_fingers(frame, convexhull, max_contour)
        return frame, fingers

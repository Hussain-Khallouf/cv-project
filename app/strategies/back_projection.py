from math import ceil
from helper import Colors
import numpy as np
from helper import HelperCV
import cv2 as cv
from cv2 import Mat


class BackProjection:
    def __init__(self, size=(400, 400), factor_of_rectangle_hand_detection_sit=1/8, ranges=[0, 180], cahnnels=[0],
                 histSize=[180],
                 disc=cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5)),
                 kernel_size=(5, 5), color=Colors.black.value, thickness=2,
                 is_opening=False, is_closing=False) -> None:
        self.is_hand_hist_taken = False
        self.size = size
        self.size_of_rec = factor_of_rectangle_hand_detection_sit
        self.start_point = tuple(
            ceil(ti/2)-ceil(ti*factor_of_rectangle_hand_detection_sit) for ti in size)
        self.end_point = tuple(
            ceil(ti/2)+ceil(ti*factor_of_rectangle_hand_detection_sit) for ti in size)
        self.histSize = histSize
        self.ranges = ranges
        self.cahnnels = cahnnels
        self.disc = disc
        self.kernel = np.ones(kernel_size, np.uint8)
        self.is_opening = is_opening
        self.is_closing = is_closing
        self.color = color
        self.thickness = thickness

    def apply(self, frame: Mat, pressed_key):

        frame = cv.resize(frame, self.size)
        thresh = frame.copy()
        if HelperCV.is_pressed(pressed_key, "z"):
            self.is_hand_hist_taken = True
            self.hist_hand = self.calculate_hist(frame)

        if HelperCV.is_pressed(pressed_key, "c"):
            self.is_closing = not self.is_closing
            print(f"is_closing : {self.is_closing}")

        if HelperCV.is_pressed(pressed_key, "o"):
            self.is_opening = not self.is_opening
            print(f"is_opening : {self.is_opening}")

        if self.is_hand_hist_taken:
            thresh, mask = self.hist_mask(frame, self.hist_hand)
            return thresh, mask
        frame = self.draw_rectangle_for_detect_hist_skin(frame)
        return thresh, frame

    def calculate_hist(self, frame):
        frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        roi = frame_hsv[self.start_point[0]:self.end_point[0],
                        self.start_point[1]:self.end_point[1]]
        hsv = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
        roihist = cv.calcHist([hsv], self.cahnnels,
                              None, self.histSize, self.ranges)
        return cv.normalize(roihist, roihist, 0, 255, cv.NORM_MINMAX)

    def hist_mask(self, frame, hist_hand):
        hsvt = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        dst = cv.calcBackProject(
            [hsvt], self.cahnnels, hist_hand, self.ranges, 1)
        cv.filter2D(dst, -1, self.disc, dst)
        _, thresh = cv.threshold(dst, 50, 255, 0)
        thresh = cv.merge((thresh, thresh, thresh))

        if self.is_closing:
            thresh = cv.morphologyEx(thresh, cv.MORPH_CLOSE, self.kernel)

        if self.is_opening:
            thresh = cv.morphologyEx(thresh, cv.MORPH_OPEN, self.kernel)

        return thresh, cv.bitwise_and(frame, thresh)

    def draw_rectangle_for_detect_hist_skin(self, frame):
        copy = cv.resize(frame, self.size)
        return cv.rectangle(copy, self.start_point,
                            self.end_point, self.color, self.thickness)

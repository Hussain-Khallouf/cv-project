import cv2 as cv
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
        self.face_cascade = FaceHaarCasade()
        self.gestures_detectors = GesturesDetectors()
        self.disc = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))

    def _face_removal(self, image, thikness=10):
        image = self.face_cascade.remove_faces(image, thikness)
        return image

    def _hand_hist_mask(self, image, hand_hist):
        hsvt = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        dst = cv.calcBackProject([hsvt], [0, 1], hand_hist, [0, 180, 0, 256], 1)
        cv.filter2D(dst, -1, self.disc, dst)
        _, thresh = cv.threshold(dst, 50, 255, 0)
        thresh = cv.merge((thresh, thresh, thresh))
        return thresh

    def _calculate_fingers(self, framez, convexhull, max_contour):
        frame = framez.copy()
        h, w = frame.shape[:2]
        min_y = h  # Set the minimum y-value equal to frame's height value
        final_point = (w, h)
        for i in range(len(convexhull)):
            point = (convexhull[i][0][0], convexhull[i][0][1])
            if point[1] < min_y:
                min_y = point[1]
                final_point = point
        # Draw a circle (black color) to the point with the minimum y-value
        cv.circle(frame, final_point, 5, Colors.black.value, 2)
        M = cv.moments(max_contour)  # Moments

        # Find the center of the max contour
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # Draw circle (red color) in the center of max contour
            cv.circle(frame, (cX, cY), 6, Colors.Red.value, 3)

        contour_poly = cv.approxPolyDP(
            max_contour, 0.01 * cv.arcLength(max_contour, True), True
        )
        # Draw contour polygon (white color)
        cv.fillPoly(frame, [max_contour], Colors.green.value)

        areahull = cv.contourArea(convexhull)
        areacnt = cv.contourArea(max_contour)
        arearatio = ((areahull - areacnt) / areacnt) * 100
        hull = cv.convexHull(contour_poly, returnPoints=False)
        defects = cv.convexityDefects(contour_poly, hull)

        l = 0

        # code for finding no. of defects due to fingers
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(contour_poly[s][0])
            end = tuple(contour_poly[e][0])
            far = tuple(contour_poly[f][0])
            pt = (100, 180)

            # find length of all sides of triangle
            a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
            s = (a + b + c) / 2
            ar = math.sqrt(s * (s - a) * (s - b) * (s - c))

            # distance between point and convex hull
            d = (2 * ar) / a

            # apply cosine rule here
            angle = math.acos((b**2 + c**2 - a**2) / (2 * b * c)) * 57

            # ignore angles > 90 and ignore points very close to convex hull(they generally come due to noise)
            if angle <= 90 and d > 30:
                l += 1
                cv.circle(frame, far, 3, [255, 0, 0], -1)

            # draw lines around hand
            cv.line(frame, start, end, [0, 255, 0], 2)

        l += 1
        return l

    def detect(self, frame: NDArray, hand_hist) -> config.Gestures:
        removed_face_frame = self._face_removal(frame)
        mask = self._hand_hist_mask(removed_face_frame, hand_hist)
        max_contour, convexhull, frame = utils.draw_convex_hull(frame, mask[:, :, 0])
        fingers = self.gestures_detectors.calculate_fingers(frame, convexhull, max_contour)
        return fingers

from enum import Enum
import cv2 as cv


class Colors(Enum):
    green = (0, 255, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)
    Blue = (0, 0, 255)
    Red = (255, 0, 0)


class HelperCV:

    @classmethod
    def is_pressed(cls, pressed_key, key):
        if type(key) == str:
            return pressed_key & 0xFF == ord(key)
        if type(key) == int:
            return pressed_key == key

    @classmethod
    def draw_convex_hull(cls, frame, thresh):
        thresh = thresh.copy()
        contours, _ = cv.findContours(
            thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        max_contour = cls.calculate_max_contour(contours)

        convhull = cls.calculate_convhull(max_contour)

        return max_contour, convhull, cv.drawContours(frame, [convhull], -1, Colors.Blue.value, 3, 2)

    @classmethod
    def calculate_convhull(cls, max_contour):
        return cv.convexHull(max_contour, returnPoints=True)

    @classmethod
    def calculate_max_contour(cls, contours):
        return max(contours, key=lambda x: cv.contourArea(x))

    @classmethod
    def draw_text(cls, frame, text, org=None, fontScale=2, font=cv.FONT_HERSHEY_SIMPLEX, color=Colors.green.value, thickness=3):
        if org == None:
            org = (0, frame.shape[1])
        return cv.putText(frame, text, org, font, fontScale,
                          color, thickness, cv.LINE_AA, False)

from enum import Enum
import cv2 as cv


class Colors(Enum):
    green = (0, 255, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)
    Blue = (0, 0, 255)
    Red = (255, 0, 0)


def calculate_convhull(max_contour):
    return cv.convexHull(max_contour, returnPoints=True)


def calculate_max_contour(contours):
    return max(contours, key=lambda x: cv.contourArea(x))


def draw_convex_hull(frame, thresh):
    thresh = thresh.copy()
    contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    max_contour = calculate_max_contour(contours)
    convhull = calculate_convhull(max_contour)

    return (
        max_contour,
        convhull,
        cv.drawContours(frame, [convhull], -1, Colors.Blue.value, 3, 2),
    )


def draw_text(
    frame,
    text,
    org=None,
    fontScale=2,
    font=cv.FONT_HERSHEY_SIMPLEX,
    color=Colors.green.value,
    thickness=3,
):
    if org == None:
        org = (0, frame.shape[1])
    return cv.putText(
        frame, text, org, font, fontScale, color, thickness, cv.LINE_AA, False
    )

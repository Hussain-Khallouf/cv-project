import traceback
from cv2 import Mat
from gestures_detectors import GesturesDetectors
from haar import HaarCasCade
from back_projection import BackProjection
from helper import HelperCV
import cv2 as cv
import numpy as np
esc_key = 27


def main():
    cap = cv.VideoCapture(0)
    backProjection = BackProjection(kernel_size=(7, 7))
    haarCasCade = HaarCasCade()
    gestures_detectors = GesturesDetectors()
    while cap.isOpened():
        pressed_key = cv.waitKey(1)
        _, frame = cap.read()
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
            fingers = gestures_detectors.calculate_fingers(
                frame, convexhull, max_contour)
            frame = HelperCV.draw_text(frame, f"{fingers}")
        except Exception as e:
            print(e)
            print(traceback.format_exc())

        view_stack = np.concatenate((
            frame, mask_cascade, thresh, view), axis=1)

        cv.imshow("The View", view_stack)

        if HelperCV.is_pressed(pressed_key, "q") or HelperCV.is_pressed(pressed_key, esc_key):
            break

    cv.destroyAllWindows()


if __name__ == "__main__":
    main()

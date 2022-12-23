from enum import Enum
import cv2 as cv


class Colors(Enum):
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    CYAN = (255, 255, 0)


class Vertical:
    UP = 0
    DOWN = 1
    STATIC = 2


class Horizontal:
    RIGHT = 0
    LEFT = 1
    STATIC = 2


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

        return max_contour, convhull, cv.drawContours(frame, [convhull], -1, Colors.BLUE.value, 3, 2)

    @classmethod
    def calculate_convhull(cls, max_contour):
        return cv.convexHull(max_contour, returnPoints=True)

    @classmethod
    def calculate_max_contour(cls, contours):
        return max(contours, key=lambda x: cv.contourArea(x))

    @classmethod
    def draw_text(cls, frame, text, org=[Horizontal.LEFT, Vertical.DOWN], fontScale=2, font=cv.FONT_HERSHEY_SIMPLEX, color=Colors.GREEN.value, thickness=3):
        pos = cls.calculate_postion_on_image(frame.shape[:2], org[0], org[1])
        # if org[0] == None:
        #     org = (0, frame.shape[1])
        return cv.putText(frame, text, pos, font, fontScale,
                          color, thickness, cv.LINE_AA, False)

    @classmethod
    def calculate_postion_on_image(cls, size: tuple[int, int], horizontal: Horizontal, vertical: Vertical):
        x, y = tuple(it/2 for it in size)
        shift = 20
        if horizontal == Horizontal.LEFT:
            x = 0+shift
        elif horizontal == Horizontal.RIGHT:
            x = size[0]-shift

        if vertical == Vertical.DOWN:
            y = size[1]-shift
        elif vertical == Vertical.UP:
            y = 0+shift

        return x, y

    @classmethod
    def draw_high_point_in_convexhull(cls, frame, convexhull):
        h, w = frame.shape[:2]
        min_y = h  # Set the minimum y-value equal to frame's height value
        final_point = (w, h)
        for i in range(len(convexhull)):
            point = (convexhull[i][0][0], convexhull[i][0][1])
            if point[1] < min_y:
                min_y = point[1]
                final_point = point
        # Draw a circle (black color) to the point with the minimum y-value
        cv.circle(frame, final_point, 8, Colors.BLACK.value, 2)
        return final_point

    @classmethod
    def caluclate_orentaion(cls, diff):
        ox, oy = None, None
        dx, dy = diff

        if (dx < 0):
            ox = "left"
        elif (dx > 0):
            ox = "right"
        else:
            ox = "static"

        if (dy < 0):
            oy = "up"
        elif (dy > 0):
            oy = "down"
        else:
            oy = "static"

        orentation = (ox, oy)
        return orentation

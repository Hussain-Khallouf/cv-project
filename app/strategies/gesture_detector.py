import math

from app.strategies.helper import Colors, HelperCV
import cv2 as cv


class GesturesDetectors:

    def __init__(self) -> None:
        self.cX = 0
        self.cY = 0
        self.center = (0, 0)
        self.diff = (0, 0)
        self.orentation = ("static", "static")
        self.angles = []
        self.endpoint = (0,0)


    def calculate_fingers(self, image, convexhull, max_contour):
        frame = image.copy()

        # draw black circle in above of the hand
        self.endpoint = HelperCV.draw_high_point_in_convexhull(frame, convexhull)

        # find center on the hand
        self.center = self.find_center_of_hand(max_contour)

        # Contour Approximation
        epsilon = 0.01*cv.arcLength(max_contour, True)
        contour_poly = cv.approxPolyDP(max_contour, epsilon, True)

        draw_poly = False
        if draw_poly:
            # Draw contour polygon (white color)
            cv.drawContours(frame, [contour_poly], 0, Colors.GREEN.value, 3)
            # cv.fillPoly(frame, [contour_poly], Colors.GREEN.value)
        else:
            # draw contours on hand
            cv.drawContours(frame, [max_contour], 0, Colors.GREEN.value, 3)

        areahull = cv.contourArea(convexhull)
        areacnt = cv.contourArea(max_contour)
        arearatio = ((areahull-areacnt)/areacnt)*100
        hull = cv.convexHull(contour_poly, returnPoints=False)
        defects = cv.convexityDefects(contour_poly,  hull)

        fingers = self.count_fingers_angels(frame, defects, contour_poly)

        # Draw circle (red color) in the center of max contour
        cv.circle(frame, self.center, 6, Colors.RED.value, 3)

        return frame, fingers

    def detection_gestuers(self, frame, fingers, areacnt, arearatio):
        font = cv.FONT_HERSHEY_SIMPLEX
        line = cv.LINE_AA
        text = " "
        if fingers == 1:
            if areacnt < 2000:
                text = 'Put hand in the box'
            else:
                if arearatio < 12:
                    text = '0'
                elif arearatio < 17.5:
                    text = 'Best of luck'
                else:
                    text = '1'
        elif fingers == 2:
            text = '2'
        elif fingers == 3:

            if arearatio < 27:
                text = '3'
            else:
                text = 'ok'

        elif fingers == 4:
            text = '4'
        elif fingers == 5:
            text = '5'
        else:
            text = 'reposition'

        cv.putText(frame, text, (10, 50),
                   font, 2, (0, 0, 255), 3, line)

        return text

    def caluclate_orentaion(self):
        self.orentation = HelperCV.caluclate_orentaion(self.diff)
        return self.orentation

    def find_center_of_hand(self, max_contour):
        M = cv.moments(max_contour)

        # Find the center of the max contour
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            self.diff = (cX-self.cX, cY-self.cY)
            self.cX = cX
            self.cY = cY
            self.center = (self.cX, self.cY)
        return self.center

    def count_fingers_angels(self, frame, defects, contour_poly):
        fingers = 0
        self.angles.clear()

        # code for finding no. of defects due to fingers
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(contour_poly[s][0])
            end = tuple(contour_poly[e][0])
            far = tuple(contour_poly[f][0])
            pt = (100, 180)

            cv.line(frame, start, far, Colors.CYAN.value, 3)
            cv.line(frame, end, far, Colors.CYAN.value, 3)

            # find length of all sides of triangle
            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)

            # find space
            s = (a+b+c)/2
            ar = math.sqrt(s*(s-a)*(s-b)*(s-c))

            # distance between point and convex hull
            d = (2*ar)/a

            # apply cosine rule here
            angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
            self.angles.append(angle)
            # ignore angles > 90 and ignore points very close to convex hull(they generally come due to noise)
            if angle <= 90 and d > 30:

                fingers += 1
                # draw between fingers
                cv.circle(frame, far, 6, Colors.BLUE.value, -1)
        fingers += 1
        return fingers
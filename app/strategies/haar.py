import cv2 as cv
from cv2 import Mat
import numpy as np


class HaarCasCade:
    def __init__(self, face_path="./haarcascade_frontalface_default.xml", thinkess=10, color=(255, 255, 255)) -> None:
        self.face_path = face_path
        self.face_cascade = cv.CascadeClassifier(face_path)
        self.thinkess = thinkess
        self.color = color

    def apply(self, frame: Mat, thinkess=10):
        copy = frame.copy()
        white = np.zeros(copy.shape, np.uint8)
        white[:] = (255, 255, 255)
        gray_frame = cv.cvtColor(copy, cv.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray_frame, scaleFactor=1.05, minNeighbors=5, minSize=(40, 40))
        for (x, y, w, h) in faces:
            cv.rectangle(white, (x-thinkess, y-thinkess), (x + w+thinkess,
                                                           y + h+thinkess), (0, 0, 0), -1)
        return white

import cv2 as cv
from cv2 import Mat


class FaceHaarCasade:
    def __init__(
        self,
        face_path="haarcascade_frontalface_default.xml",
        thinkess=10,
        color=(255, 255, 255),
    ) -> None:
        self.face_path = face_path
        self.face_cascade = cv.CascadeClassifier(cv.data.haarcascades + face_path)
        self.thinkess = thinkess
        self.color = color

    def remove_faces(self, frame: Mat, thinkess=10):
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray_frame, scaleFactor=1.05, minNeighbors=5, minSize=(40, 40)
        )
        for (x, y, w, h) in faces:
            cv.rectangle(
                frame,
                (x - thinkess, y - thinkess),
                (x + w + thinkess, y + h + thinkess),
                (0, 0, 0),
                -1,
            )
        return frame

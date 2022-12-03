import numpy as np
from tkinter import *
from PIL import Image, ImageTk
from numpy._typing import NDArray
import cv2


class EditorWindow:
    def __init__(self, main_image: NDArray):
        self.master = Toplevel()
        self.main_image = main_image
        img = self._npimage2tkimage(main_image)

        self.main_label = Label(self.master, image=img)
        # self.main_label = Label(master, text="hello")
        self.main_label.pack()
        self.master.mainloop()

    def _npimage2tkimage(self, image: NDArray):
        # b, g, r = image[:, :, 0], image[:, :, 1], image[:, :, 2]  # For RGB image
        # img = np.dstack([r, g, b])
        im = Image.fromarray(image)
        return ImageTk.PhotoImage(image=im)

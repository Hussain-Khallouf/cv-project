import numpy as np
from tkinter import *
from PIL import Image, ImageTk
from numpy._typing import NDArray


class EditorWindow:
    def __init__(self, master: Tk, main_image: NDArray):
        self.master = master
        self.main_image = main_image
        img = self._npimage2tkimage(main_image)
        self.main_label = Label(master, image=img)
        # self.main_label = Label(master, text="hello")
        self.main_label.pack()

    def _npimage2tkimage(self, image: NDArray):
        b, g, r = image[:, :, 0], image[:, :, 1], image[:, :, 2]  # For RGB image
        img = np.dstack([r, g, b])
        im = Image.fromarray(img)
        return ImageTk.PhotoImage(image=im)

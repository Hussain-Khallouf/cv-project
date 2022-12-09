import numpy as np
import PIL.Image
from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo, showerror
from app.config import config
from app.image_editor import ImageEditor
from .editor_window import EditorWindow


import cv2


class MainWindow:
    def __init__(self, image_editor: ImageEditor):
        self.image_editor = image_editor
        self.master = Tk()
        self.selected_image_path = None
        self.master.geometry("400x400")
        self.file_dialog_bt = Button(
            self.master, text="Choose an image", command=self._select_file_dialog
        )
        self.file_dialog_bt.pack()
        self.start_bt = Button(
            self.master, text="Start", command=self.start, foreground="red"
        )
        self.start_bt.pack()
        self.master.mainloop()

    def _select_file_dialog(self):
        filename = fd.askopenfilename(
            title="Select an image", initialdir="/", filetypes=config.image_file_types
        )
        showinfo(title="Selected Image", message=filename)
        self.selected_image_path = filename

    def start(self):
        if not self.selected_image_path:
            showerror(
                title="There is no image", message="You did not choose an image to edit"
            )
            return
        # self.master.destroy()
        pil_image = PIL.Image.open("robot_football.jpg").convert("RGB")
        selected_image = np.array(pil_image)

        # selected_image = cv2.imread(self.selected_image_path)

        EditorWindow(main_image=selected_image)

        # should be moved to another function

        """
        open the selected image
        instantiate EditorWindow class
        loop:
            take a frame from camera  
            detect a gesture by strategy
            apply the corresponding action
            update gui
        """

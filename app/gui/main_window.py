import cv2
import numpy as np
from tkinter import *
from tkinter import ttk
from numpy._typing import NDArray
from PIL import ImageTk, Image as PILImage
from threading import Thread
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo, showerror

from app.config import config
from app.image_editor import ImageEditor
from app.strategies.gestures_detection_strategy import  GestureDetectionStrategy
from app.config.config import gesture2action
class MainWindow:
    def __init__(self, image_editor: ImageEditor = None):

        # TODO: must be moved to deps
        self.gesture_strategy = GestureDetectionStrategy()



        self.WORK_PLACE_WIDTH = 1600
        self.WORK_PLACE_HEIGHT = 1400

        self.image_editor = image_editor
        self.master = Tk()
        self.master.title("cv-project")
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.master.geometry(f'{screen_width}x{screen_height}')
        self.master.resizable(True, True)

        self.file_dialog_bt = Button(
            self.master, text="Choose an image", command=self._select_file_dialog
        )
        self.file_dialog_bt.place(relx=0.01, rely=0.4)

        self.start_bt = Button(
            self.master, text="Start", command=self.start, foreground="red"
        )
        self.start_bt.place(relx=0.01, rely=0.45)
        self.save_bt = Button(
            self.master, text="Save", command=self.save, foreground="green", state=DISABLED
        )
        self.save_bt.place(relx=0.01, rely=0.5)

        self.workplace_label = Label(self.master, text="Image")
        self.workplace_label.pack(side=TOP, anchor="e", padx=2, pady=2)

        self.camera_label = Label(self.master, text="Camera", )
        self.camera_label.place(x=0, y=0)

        self.selected_image_path = None
        self.workplace = np.zeros((self.WORK_PLACE_HEIGHT, self.WORK_PLACE_WIDTH, 3), dtype=np.uint8)

        self._update_workplace_label(self.workplace)

        self.master.mainloop()

    def _set_image_in_workplace(self, image: NDArray):
        if self.WORK_PLACE_WIDTH < image.shape[1] or self.WORK_PLACE_HEIGHT < image.shape[0]:
            raise ValueError("Dimensions Error")
        self.workplace[:image.shape[0], :image.shape[1], :] = image

    def _tuning_image_scale(self, image: NDArray):
        if self.WORK_PLACE_WIDTH < image.shape[1]:
            scale = image.shape[1] / self.WORK_PLACE_WIDTH
            new_width = int(image.shape[1] / scale)
            new_height = int(image.shape[0] / scale)
            image = cv2.resize(image, (new_width, new_height))
        if self.WORK_PLACE_HEIGHT < image.shape[0]:
            scale = image.shape[1] / self.WORK_PLACE_HEIGHT
            new_width = int(image.shape[1] / scale)
            new_height = int(image.shape[0] / scale)
            image = cv2.resize(image, (new_width, new_height))
        return image

    def _select_file_dialog(self):
        filename = fd.askopenfilename(
            title="Select an image", initialdir="/", filetypes=config.image_file_types
        )
        showinfo(title="Selected Image", message=filename)
        self.selected_image_path = filename
        self._set_image_filepath(self.selected_image_path)

    def _npimage2tkimage(self, image: NDArray):  # convert from NDArray to ImageTk from viewing on image label
        b, g, r = image[:, :, 0], image[:, :, 1], image[:, :, 2]  # For RGB image
        img = np.dstack([r, g, b])
        im = PILImage.fromarray(img)
        return ImageTk.PhotoImage(image=im)

    def _set_camera_image(self, image: ImageTk.PhotoImage):
        self.camera_label.configure(image=image)
        self.camera_label.image = image

    def _update_workplace_label(self, image: NDArray):
        tk_image = self._npimage2tkimage(image)
        self.workplace = np.zeros((self.WORK_PLACE_HEIGHT, self.WORK_PLACE_WIDTH, 3), dtype=np.uint8)
        self.workplace_label.configure(image=tk_image)
        self.workplace_label.image = tk_image

    def _set_image_filepath(self, filepath):
        image = cv2.imread(filepath)
        image = self._tuning_image_scale(image)
        self._set_image_in_workplace(image)
        self._update_workplace_label(self.workplace)

    def run(self):
        capture = cv2.VideoCapture(0)
        # capture.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
        # capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        if capture.isOpened():
            while True:
                flag, frame = capture.read()
                # TODO: 1 recognize hand gesture for "frame" using
                gesture = self.gesture_strategy.detect(frame)
                # TODO: 2 apply the corresponding action
                action = gesture2action.get(gesture.value, None)
                # TODO: 3 Update self.workpalce using "_update_workplace_label" function


                camera_image = cv2.resize(frame, (310, 240))
                tk_image = self._npimage2tkimage(camera_image)
                self._set_camera_image(tk_image)

    def start(self):
        if not self.selected_image_path:
            showerror(
                title="There is no image", message="You did not choose an image to edit"
            )
            return

        self.file_dialog_bt["state"] = "disabled"
        self.save_bt["state"] = "active"
        self.image_editor.set_image(self.workplace)
        Thread(target=self.run).start()

    def save(self):
        pass

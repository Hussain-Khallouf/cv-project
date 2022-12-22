import cv2 as cv
import numpy as np
from tkinter import *
from numpy._typing import NDArray
from PIL import ImageTk, Image as PILImage
from threading import Thread
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo, showerror

from app.config import config
from app.image_editor import ImageEditor
from app.strategies.gestures_detection_strategy import GestureDetectionStrategy


class MainWindow:
    def __init__(self, image_editor: ImageEditor = None):
        self.camera_frame_size = (1280, 820)
        self.gesture_strategy = GestureDetectionStrategy()

        self.image_editor = image_editor
        self.master = Tk()
        self.master.title("cv-project")
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.WORK_PLACE_WIDTH = int(screen_width * 0.8)
        self.WORK_PLACE_HEIGHT = int(screen_height * 0.95)
        self.master.geometry(f"{screen_width}x{screen_height}")
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
            self.master,
            text="Save",
            command=self.save,
            foreground="green",
            state=DISABLED,
        )
        self.save_bt.place(relx=0.01, rely=0.5)
        self.translate_bt = Button(
            self.master,
            text="translate",
            command=self.bt_tr,
            foreground="green",
        )
        self.translate_bt.place(relx=0.01, rely=0.6)

        self.rotate_bt = Button(
            self.master,
            text="rotate",
            command=self.bt_ro,
            foreground="green",
        )
        self.rotate_bt.place(relx=0.01, rely=0.7)
        self.scale_bt = Button(
            self.master,
            text="scale",
            command=self.bt_sc,
            foreground="green",
        )
        self.scale_bt.place(relx=0.01, rely=0.8)

        self.workplace_label = Label(self.master, text="Image")
        self.workplace_label.pack(side=TOP, anchor="e", padx=2, pady=2)

        self.camera_label = Label(
            self.master,
            text="Camera",
        )
        self.camera_label.place(x=0, y=0)

        self.selected_image_path = None
        self.workplace = np.zeros(
            (self.WORK_PLACE_HEIGHT, self.WORK_PLACE_WIDTH, 3), dtype=np.uint8
        )

        self._update_workplace_label(self.workplace)

        self.master.mainloop()

    def bt_tr(self):
        self.image_editor.add_action(config.Actions.TRANSLATE_HORIZONTAL, {})

    def bt_ro(self):
        self.image_editor.add_action(config.Actions.ROTATE, {})

    def bt_sc(self):
        self.image_editor.add_action(config.Actions.SCALE, {})

    def _set_image_in_workplace(self, image: NDArray):
        # if (
        #         self.WORK_PLACE_WIDTH < image.shape[1]
        #         or self.WORK_PLACE_HEIGHT < image.shape[0]
        # ):
        #     raise ValueError("Dimensions Error")
        h, w = image.shape[:2]
        h1, w1 = self.workplace.shape[:2]

        rows = max(h1, h) - h
        cols = max(w1, w) - w

        above = rows // 2
        bottom = rows - above

        left = cols // 2
        right = cols - left

        image = np.pad(image, ((above, bottom), (left, right), (0, 0)), 'constant', constant_values=0)

        h, w = image.shape[:2]

        yoff = round((h - h1) / 2)
        xoff = round((w - w1) / 2)

        self.workplace = image[yoff:yoff + h1, xoff:xoff + w1]

    def _tuning_image_scale(self, image: NDArray):
        if self.WORK_PLACE_WIDTH < image.shape[1]:
            scale = image.shape[1] / self.WORK_PLACE_WIDTH
            new_width = int(image.shape[1] / scale)
            new_height = int(image.shape[0] / scale)
            image = cv.resize(image, (new_width, new_height))
        if self.WORK_PLACE_HEIGHT < image.shape[0]:
            scale = image.shape[1] / self.WORK_PLACE_HEIGHT
            new_width = int(image.shape[1] / scale)
            new_height = int(image.shape[0] / scale)
            image = cv.resize(image, (new_width, new_height))
        return image

    def _select_file_dialog(self):
        filename = fd.askopenfilename(
            title="Select an image", initialdir="/", filetypes=config.image_file_types
        )
        showinfo(title="Selected Image", message=filename)
        self.selected_image_path = filename
        self._set_image_filepath(self.selected_image_path)

    def _npimage2tkimage(
            self, image: NDArray
    ):  # convert from NDArray to ImageTk from viewing on image label
        b, g, r = image[:, :, 0], image[:, :, 1], image[:, :, 2]  # For RGB image
        img = np.dstack([r, g, b])
        im = PILImage.fromarray(img)
        return ImageTk.PhotoImage(image=im)

    def _set_camera_image(self, image: ImageTk.PhotoImage):
        self.camera_label.configure(image=image)
        self.camera_label.image = image

    def _update_workplace_label(self, image: NDArray):
        tk_image = self._npimage2tkimage(image)
        # self.workplace = np.zeros(
        #     (self.WORK_PLACE_HEIGHT, self.WORK_PLACE_WIDTH, 3), dtype=np.uint8
        # )
        self.workplace_label.configure(image=tk_image)
        self.workplace_label.image = tk_image

    def _set_image_filepath(self, filepath):
        image = cv.imread(filepath)
        image = self._tuning_image_scale(image)
        self._set_image_in_workplace(image)
        self._update_workplace_label(self.workplace)
        self.image_editor.set_image(self.workplace)

    def tuning_hist(self):
        capture = cv.VideoCapture(0)
        ROI_start_position = (1000, 100)
        ROI_end_position = (1200, 300)
        roihist = None
        if capture.isOpened():
            while True:
                flag, frame = capture.read()
                if not flag:
                    break
                frame = cv.flip(frame, 1)
                frame = cv.resize(frame, self.camera_frame_size)

                if cv.waitKey(1) == ord("z"):
                    roi = frame.copy()[
                          ROI_start_position[1]: ROI_end_position[1],
                          ROI_start_position[0]: ROI_end_position[0],
                          ]
                    roi = cv.resize(roi, self.camera_frame_size)
                    hsv = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
                    roihist = cv.calcHist(
                        [hsv], [0, 1], None, [180, 256], [0, 180, 0, 256]
                    )
                    roihist = cv.normalize(roihist, roihist, 0, 255, cv.NORM_MINMAX)
                    break
                cv.rectangle(
                    frame, ROI_start_position, ROI_end_position, (0, 0, 255), 2
                )
                cv.imshow("tuning", frame)
            capture.release()
            cv.destroyAllWindows()
        return roihist

    def apl_action(self, fingers, min_pos, max_pos):
        if fingers == 5:
            self.image_editor.add_action(config.Actions.TRANSLATE_HORIZONTAL,
                                         {"value": int((max_pos[0] - min_pos[0]) * 0.1)})
            self.image_editor.add_action(config.Actions.TRANSLATE_VERTICAL,
                                         {"value": int((max_pos[1] - min_pos[1]) * 0.1)})
        if fingers == 3:
            self.image_editor.add_action(config.Actions.ROTATE, {})
        if fingers == 1:
            self.image_editor.add_action(config.Actions.SCALE, {})

    def run(self):
        hist = self.tuning_hist()
        capture = cv.VideoCapture(0)
        i = 0
        frame_fingers = []
        min_pos, max_pos = None, None
        if capture.isOpened():
            while True:
                flag, frame = capture.read()
                frame = cv.flip(frame, 1)
                # frame = cv.resize(frame, self.camera_frame_size)
                try:
                    frame, fingers, center = self.gesture_strategy.detect(frame, hist)
                    cv.putText(frame, str(fingers), (0, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv.LINE_AA)
                except:
                    continue
                frame_fingers.append(fingers)
                if i == 0:
                    min_pos = center
                if i >= 10:
                    max_pos = center
                    f = max(frame_fingers)
                    c = frame_fingers.count(f)
                    if c >= 5:
                        self.apl_action(f, min_pos, max_pos)
                    i = 0
                    frame_fingers = []
                i += 1
                # self.apl_action(fingers)
                camera_image = cv.resize(frame, (310, 240))
                tk_image = self._npimage2tkimage(camera_image)
                self._set_camera_image(tk_image)

                edited_image = self.image_editor.get_edited_image()
                # edited_image = self._tuning_image_scale(edited_image)
                self._set_image_in_workplace(edited_image)
                self._update_workplace_label(self.workplace)
                cv.waitKey(10)

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
        img = self.image_editor.get_edited_image()
        cv.imwrite("edited.jpg", img)

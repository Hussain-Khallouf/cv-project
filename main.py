from app.gui.main_window import MainWindow
import cv2 as cv
from app import deps

if __name__ == "__main__":
    image_editor = deps.get_image_editor()
    MainWindow(image_editor)


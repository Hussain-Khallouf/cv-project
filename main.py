from app.gui.main_window import MainWindow
from app import deps
from tkinter import Tk

if __name__ == "__main__":
    image_editor = deps.get_image_editor()
    MainWindow(image_editor)

from app.gui.main_window import MainWindow
from app import deps
from tkinter import Tk

if __name__ == "__main__":
    root = Tk()
    ie = deps.get_image_editor()
    MainWindow(root, ie)
    root.mainloop()

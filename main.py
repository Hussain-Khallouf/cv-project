from app.gui.main_window import MainWindow
import cv2 as cv
from app import deps

if __name__ == "__main__":
    image = cv.imread("robot_football.jpg")
    cv.imshow("original_image", image)
    image_editor = deps.get_image_editor()
    image_editor.set_image(image)
    for i in range(20):
        image_editor.blurring()
    edited_image = image_editor.get_edited_image()
    cv.imshow("blurring_20_times", edited_image)
    for i in range(20):
        image_editor.undo()
    edited_image = image_editor.get_edited_image()
    cv.imshow("undo_20_times", edited_image)
    for i in range(5):
        image_editor.redo()
    edited_image = image_editor.get_edited_image()
    cv.imshow("redo_5_times", edited_image)

    cv.waitKey(0)

from app.repo.image_repo import Image
from app.usecases.editor_usesaces import EditorUS
from app.controller.image_controller import ImageController
from app.image_editor import ImageEditor
from app.strategies.gestures_detection_strategy import (
    GestureDetectionStrategy,
    # MLGestureDetectionStrategy,
)


def get_image_repo():
    return Image()


def get_editor_usecases() -> EditorUS:
    return EditorUS(ImageController())


def get_image_editor():
    return ImageEditor(editor_uc=get_editor_usecases())


# def get_gesture_detection_strategy() -> GestureDetectionStrategy:
#     return MLGestureDetectionStrategy()

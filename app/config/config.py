"""
global config and types
"""

from enum import Enum


image_file_types = [("image files", ".png"), ("image files", ".jpg")]

class Gestures(Enum):
    LIKE = 0
    TWO_FINGERS = 1




class Actions(Enum):
    TRANSLATE_LEFT = 1
    TRANSLATE_RIGHT = 2
    TRANSLATE_TOP = 3
    TRANSLATE_BOTTOM = 4
    BLURRING = 5


gesture2action = {
    Gestures.LIKE.value: Actions.BLURRING,
    Gestures.TWO_FINGERS.value: Actions.TRANSLATE_TOP
}

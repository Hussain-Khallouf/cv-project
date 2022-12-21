"""
global config and types
"""

from enum import Enum


image_file_types = [("image files", ".png"), ("image files", ".jpg")]

class Gestures(Enum):
    LIKE = 0
    FIVE_FINGERS = 5
    TWO_FINGERS = 2
    THREE_FINGERS = 3
    FOUR_FINGERS = 4
    ONE_FINGERS = 1




class Actions(Enum):
    TRANSLATE = 5
    ROTATE = 2
    SCALE = 3
    SKEW = 3
    WARP = 1
    # BLURRING = 1


gesture2action = {
    Gestures.LIKE.value: Actions.BLURRING,
    Gestures.FIVE_FINGERS.value: Actions.TRANSLATE,
    Gestures.TWO_FINGERS.value: Actions.ROTATE,
    Gestures.THREE_FINGERS.value: Actions.SCALE,
    Gestures.FOUR_FINGERS.value: Actions.SKEW,
}

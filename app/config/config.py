"""
global config and types
"""

from enum import Enum

image_file_types = [("image files", ".png"), ("image files", ".jpg")]


class Gestures(Enum):
    # LIKE = 0
    EMPTY = -1
    ONE_FINGERS = 1
    TWO_FINGERS = 2
    THREE_FINGERS = 3
    FOUR_FINGERS = 4
    FIVE_FINGERS = 5


class Actions(Enum):
    NO_ACTION = -1
    WARP = 1
    ROTATE = 2
    SCALE = 3
    SKEW = 4
    TRANSLATE_VERTICAL = 5
    TRANSLATE_HORIZONTAL = 6
    BLURRING = 8


gesture2action = {
    # Gestures.LIKE.value: Actions.BLURRING,
    Gestures.FIVE_FINGERS.value: Actions.TRANSLATE_HORIZONTAL,
    Gestures.TWO_FINGERS.value: Actions.ROTATE,
    Gestures.THREE_FINGERS.value: Actions.SCALE,
    Gestures.FOUR_FINGERS.value: Actions.SKEW,
    Gestures.EMPTY.value: Actions.NO_ACTION,
}

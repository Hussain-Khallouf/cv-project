"""
global config and types
"""

from enum import Enum

image_file_types = [
    ("image files", ".png"),
    ("image files", ".jpg")
]


class Gestures(Enum):
    like = "like"


class Actions(Enum):
    blurring = "blurring"


gesture2action = {
    Gestures.like.value: Actions.blurring
}

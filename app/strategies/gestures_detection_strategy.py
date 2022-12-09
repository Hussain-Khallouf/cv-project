from numpy._typing import NDArray
from app.config import config


class GestureDetectionStrategy:
    """
    abstract class for strategy design pattern
    you can implement gesture detection strategy as many as you want by inheriting from  this class
    """

    def detect(self, Image: NDArray) -> config.Gestures:
        pass


class MLGestureDetectionStrategy:
    """
    machine learning strategy
    """

    pass

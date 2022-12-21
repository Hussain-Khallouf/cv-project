from numpy._typing import NDArray
from app.config import config


class GestureDetectionStrategy:
    """
    abstract class for strategy design pattern
    you can implement gesture detection strategy as many as you want by inheriting from  this class
    """

    def detect(self, frame: NDArray) -> config.Gestures:
        # return config.Gestures.LIKE
        pass


# example
#
# class MLGestureDetectionStrategy(GestureDetectionStrategy):
#     """
#     machine learning strategy
#     """
#     def detect(self, Image: NDArray) -> config.Gestures:
#         pass

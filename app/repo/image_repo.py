from numpy._typing import NDArray


class Image:
    _image: NDArray = None

    def set_image(self, image: NDArray) -> None:
        self._image = image

    def get_image(self) -> NDArray:
        if self._image is None:
            raise IndexError("There is no image ")
        return self._image

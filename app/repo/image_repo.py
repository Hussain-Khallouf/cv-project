from numpy._typing import NDArray


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class BiLinkedList:
    def __init__(self) -> None:
        self._head = None
        self._count = 0

    def push(self, data: object) -> "BiLinkedList":
        new_node = Node(data)
        if self._head:
            self._head.next = new_node
            new_node.prev = self._head
        self._head = new_node
        self._count += 1
        return self

    def pop(self) -> Node:
        head = self._head
        self._head = self._head.prev if self._head else None
        self._count -= 1
        return head

    def go_backward(self) -> "BiLinkedList":
        self._head = self._head.prev if self._head else self._head
        return self

    def go_forward(self) -> "BiLinkedList":
        self._head = self._head.next if self._head else self._head
        return self


class ImageRepo(BiLinkedList):
    def push(self, image: NDArray) -> "ImageRepo":
        return super().push(image)

    def get_current_image(self) -> NDArray:
        if not self._head:
            raise IndexError("There is images in the Image Repository")
        return self._head.data

# this is an object oriented abstraction of the heapq library I wrote.
# I use it for a lot of projects.


from typing import Any
import heapq
from abc import ABC, abstractmethod


class QueueItem:
    """wrapper class used internally"""
    def __init__(self, priority: int, value: Any):
        self.priority = priority
        self.value = value

    def __lt__(self, item: "QueueItem") -> bool:
        if not isinstance(item, QueueItem):
            raise ValueError("QueueItem can only be compared to QueueItem")
        else:
            return self.priority < item.priority


class AbstractHeap(ABC):
    """abstract class for heap obejct"""
    def __init__(self, items=()):
        self._heap = []
        for item in items:
            self.push(item)

    def __repr__(self):
        return f"{self.__class__.__name__}(items={self._heap})"

    def __len__(self):
        return len(self._heap)

    @property
    def empty(self) -> bool:
        """whether there are any items in the heap"""
        return not len(self._heap)

    def peak(self) -> Any:
        """returns the top item without removing it from the heap"""
        return self._heap[0].value

    def pop(self) -> Any:
        """removes the top item from the heap and returns it"""
        return heapq.heappop(self._heap).value

    @abstractmethod
    def push(self, item: Any, priority: int = None) -> None:
        pass


class MinHeap(AbstractHeap):
    """The min heap datastructure
        Args:
            items: an iterable of objects to push to the heap, note that to specify priority values for item, you have
                to use the .push() method directly
        """
    def __init__(self, items=()):
        super().__init__(items)

    def push(self, item: Any, priority: int = None) -> None:
        """pushes an item to the heap
        Args:
            item: object to add
            priority: comparison value for the object, if None or unspecified, defaults to item
        """
        if priority is None:
            priority = item
        heapq.heappush(self._heap, QueueItem(priority, item))


class MaxHeap(AbstractHeap):
    """The max heap datastructure
    Args:
        items: an iterable of objects to push to the heap, note that to specify priority values for item, you have
            to use the .push() method directly
    """
    def __init__(self, items=()):
        super().__init__(items)

    def push(self, item: Any, priority: int = None) -> None:
        """pushes an item to the heap
        Args:
            item: object to add
            priority: comparison value for the object, if None or unspecified, defaults to item
        """
        if priority is None:
            priority = item
        heapq.heappush(self._heap, QueueItem(-priority, item))

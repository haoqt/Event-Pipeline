import multiprocessing as mp
from queue import Full, Empty


class BoundedQueue:
    def __init__(self, max_size: int, strategy: str = "drop"):
        self._queue = mp.Queue(maxsize=max_size)
        self.strategy = strategy

    def put(self, item) -> bool:
        if self.strategy == "block":
            self._queue.put(item)
            return True

        # drop strategy
        try:
            self._queue.put(item, block=False)
            return True
        except Full:
            return False

    def get(self, timeout=None):
        return self._queue.get(timeout=timeout)

    def size(self) -> int:
        return self._queue.qsize()
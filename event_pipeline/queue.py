from collections import deque

class BoundedQueue:
    def __init__(self, max_size: int):
        self.max_size = max_size
        self._queue = deque()
        self.dropped = 0

    def put(self, item) -> bool:
        if len(self._queue) >= self.max_size:
            self.dropped += 1
            return False
        self._queue.append(item)
        return True

    def is_full(self):
        if len(self._queue) >= self.max_size:
            return True
        return False

    def get(self):
        if not self._queue:
            return None
        return self._queue.popleft()

    def size(self):
        return len(self._queue)

    def queue_usage(self):
        return len(self._queue) / self.max_size

    
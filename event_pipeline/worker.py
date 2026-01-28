import time
from collections import defaultdict


class Worker:
    def __init__(self, worker_id: int, window_seconds: int):
        self.worker_id = worker_id
        self.window_seconds = window_seconds
        self.state = defaultdict(int)
        self.window_start = time.time()
        self.processed = 0

    def process(self, event):
        self.processed += 1
        self.state["count"] += 1
        self.state[f"status_{event.status}"] += 1
        self.state["latency_sum"] += event.latency_ms

    def maybe_flush(self):
        now = time.time()
        if now - self.window_start >= self.window_seconds:
            self.flush()
            self.window_start = now
            self.state.clear()

    def flush(self):
        print(
            f"🧱 Worker {self.worker_id} | "
            f"events={self.processed} | "
            f"state={dict(self.state)}"
        )
import multiprocessing as mp
import time
from queue import Empty

from event_pipeline.worker import Worker


def worker_loop(worker_id, queue, window_seconds):
    worker = Worker(worker_id, window_seconds)
    while True:
        try:
            event = queue.get(timeout=1)
            worker.process(event)
            worker.maybe_flush()
        except Empty:
            worker.maybe_flush()


class WorkerPool:
    def __init__(self, n_workers, queue_cls, window_seconds):
        self.queues = [queue_cls() for _ in range(n_workers)]
        self.processes = []
        self.window_seconds = window_seconds

    def start(self):
        for i, q in enumerate(self.queues):
            p = mp.Process(
                target=worker_loop,
                args=(i, q, self.window_seconds),
                daemon=True,
            )
            p.start()
            self.processes.append(p)
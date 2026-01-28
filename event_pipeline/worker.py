import time
from event_pipeline.processing import process_event
from event_pipeline.stats import WorkerStats

SNAPSHOT_INTERVAL = 1.0  # seconds

def worker_loop(queue, out_queue, worker_id: int):
    stats = WorkerStats()
    last_snapshot = time.time()

    while True:
        event = queue.get()
        if event is None:
            break

        process_event(event)
        stats.update(event)

        now = time.time()
        if now - last_snapshot >= SNAPSHOT_INTERVAL:
            out_queue.put(stats.snapshot_and_reset())
            last_snapshot = now

    # final snapshot
    out_queue.put(stats.snapshot_and_reset())
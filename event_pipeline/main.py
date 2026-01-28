import time
import threading
import uvicorn

from event_pipeline.config import (
    N_WORKERS,
    QUEUE_MAX_SIZE,
    QUEUE_STRATEGY,
    WINDOW_SECONDS,
    METRICS_LOG_INTERVAL,
)
from event_pipeline.ingest import Ingestor
from event_pipeline.queue import BoundedQueue
from event_pipeline.worker_pool import WorkerPool
from event_pipeline.metrics import Metrics

import event_pipeline.api as api


def main():
    metrics = Metrics()
    ingestor = Ingestor(metrics)

    def make_queue():
        return BoundedQueue(QUEUE_MAX_SIZE, QUEUE_STRATEGY)

    pool = WorkerPool(
        N_WORKERS,
        make_queue,
        WINDOW_SECONDS,
    )
    pool.start()

    # Inject dependency cho FastAPI
    api.ingestor = ingestor
    api.worker_queues = pool.queues
    api.metrics = metrics

    print("🚀 Pipeline started")

    # Run FastAPI trong thread riêng
    threading.Thread(
        target=lambda: uvicorn.run(
            api.app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
        ),
        daemon=True,
    ).start()

    # Metrics loop
    while True:
        metrics.maybe_log(METRICS_LOG_INTERVAL)
        time.sleep(1)


if __name__ == "__main__":
    main()
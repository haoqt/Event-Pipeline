from multiprocessing import Queue, cpu_count

NUM_WORKERS = cpu_count()

QUEUE_SIZE = 20_000  # per worker

WORKER_QUEUES = [
    Queue(maxsize=QUEUE_SIZE)
    for _ in range(NUM_WORKERS)
]

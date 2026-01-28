from queues import WORKER_QUEUES, NUM_WORKERS

def dispatch(event) -> bool:
    """
    Decide which worker handles this event.
    Non-blocking.
    """
    idx = hash(event.endpoint) % NUM_WORKERS
    queue = WORKER_QUEUES[idx]

    try:
        queue.put_nowait(event)
        return True
    except Exception:
        return False

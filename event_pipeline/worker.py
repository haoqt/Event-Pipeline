from event_pipeline.processing import process_event

def worker_loop(queue, worker_id: int):
    processed = 0

    while True:
        event = queue.get()
        if event is None:
            break

        # simulate CPU-bound work
        process_event(event)
        processed += 1

    print(f"[Worker {worker_id}] processed={processed}")
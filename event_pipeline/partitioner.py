def partition(event, n_workers: int) -> int:
    key = f"{event.service}:{event.endpoint}"
    return hash(key) % n_workers
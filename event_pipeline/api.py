from fastapi import FastAPI, HTTPException
from event_pipeline.ingest import Ingestor
from event_pipeline.partitioner import partition
from event_pipeline.config import N_WORKERS

app = FastAPI(title="Event Pipeline API")

# Những object này sẽ được inject từ main.py
ingestor: Ingestor = None
worker_queues = None
metrics = None


@app.post("/events")
def ingest_event(payload: dict):
    global ingestor, worker_queues, metrics

    event = ingestor.parse(payload)
    if not event:
        raise HTTPException(status_code=400, detail="Invalid event")

    idx = partition(event, N_WORKERS)
    ok = worker_queues[idx].put(event)

    if not ok:
        metrics.inc("queue_drop")
        raise HTTPException(status_code=429, detail="Queue full")

    metrics.inc("event_in")
    return {"status": "ok"}
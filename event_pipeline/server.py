from fastapi import FastAPI, Request, Response
from http import HTTPStatus

from event import Event
from dispatcher import dispatch
from backpressure import BackpressureController, Policy
from queues import WORKER_QUEUES
from metrics import inc_accept, inc_drop

app = FastAPI()

backpressure = BackpressureController(
    policy=Policy.SAMPLE,
    sample_rate=0.1
)

@app.post("/ingest")
async def ingest(req: Request):
    payload = await req.json()

    event = Event(
        endpoint=payload["endpoint"],
        status=payload["status"],
        latency=payload["latency"],
    )

    total_used = sum(q.qsize() for q in WORKER_QUEUES)
    total_capacity = sum(q._maxsize for q in WORKER_QUEUES)
    queue_usage = total_used / total_capacity

    if not backpressure.should_accept(queue_usage, event):
        inc_drop()
        return Response(status_code=HTTPStatus.TOO_MANY_REQUESTS)

    if not dispatch(event):
        inc_drop()
        return Response(status_code=HTTPStatus.TOO_MANY_REQUESTS)

    inc_accept()
    return {"status": "ok"}
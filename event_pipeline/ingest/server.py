## Phase 1
# from http.server import BaseHTTPRequestHandler, HTTPServer
# import json
#
# from event_pipeline.queue import BoundedQueue
# from event_pipeline.event import Event
# from .validator import validate_event
# from .normalize import normalize_endpoint
# from .ratelimit import RateLimiter
# from event_pipeline.metrics import inc_accept, inc_drop
#
# queue = BoundedQueue(max_size=1_000_000)
# rate_limiter = RateLimiter(rate_per_sec=50_000)
#
# class IngestHandler(BaseHTTPRequestHandler):
#     def do_POST(self):
#         if self.path != "/events":
#             self.send_response(404)
#             self.end_headers()
#             return
#
#         if not rate_limiter.allow():
#             self.send_response(429)
#             self.end_headers()
#             return
#
#         length = int(self.headers.get("Content-Length", 0))
#         body = self.rfile.read(length)
#
#         try:
#             data = json.loads(body)
#         except json.JSONDecodeError:
#             self.send_response(400)
#             self.end_headers()
#             return
#
#         if not validate_event(data):
#             self.send_response(400)
#             self.end_headers()
#             return
#
#         event = Event(
#             endpoint=normalize_endpoint(data["endpoint"]),
#             status=data["status"],
#             latency=data["latency_ms"],
#         )
#         if not queue.put(event):
#             self.send_response(503)  # backpressure signal
#             self.end_headers()
#             return
#
#         self.send_response(202)
#         self.end_headers()
#
# def run():
#     server = HTTPServer(("0.0.0.0", 8000), IngestHandler)
#     server.serve_forever()


## Phase 1.5
import time
from fastapi import FastAPI, Request, Response
from http import HTTPStatus
from event_pipeline.event import Event
from event_pipeline.shared import queue
from event_pipeline.backpressure import BackpressureController, Policy
from event_pipeline.metrics import inc_accept, inc_drop

import threading
from event_pipeline.consumer_loop import run as run_consumer

app = FastAPI()
backpressure = BackpressureController(
    policy=Policy.DROP,
    sample_rate=0.1,  # keep 10% khi overload
)

@app.post("/ingest")
async def ingest(req: Request):
    payload = await req.json()

    event = Event(
        endpoint=payload["endpoint"],
        status=payload["status"],
        latency=payload["latency_ms"],
    )
    queue_usage = queue.queue_usage()

    if not backpressure.should_accept(queue_usage, event):
        inc_drop()
        return Response(
            status_code=HTTPStatus.TOO_MANY_REQUESTS,
            content="dropped by backpressure",
        )

    try:
        queue.put(event)
        inc_accept()
    except Full:
        inc_drop()
        return Response(
            status_code=HTTPStatus.TOO_MANY_REQUESTS,
            content="queue full",
        )

    return {"status": "accepted"}


@app.post("/config/backpressure")
def update_policy(policy: str, sample_rate: float = 1.0):
    backpressure.policy = Policy(policy)
    backpressure.sample_rate = sample_rate


def run_with_worker():
    # Chạy consumer trong thread riêng
    worker = threading.Thread(target=run_consumer, daemon=True)
    worker.start()

    # Chạy server
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    run_with_worker()

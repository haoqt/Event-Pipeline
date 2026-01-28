from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from event_pipeline.queue import BoundedQueue
from event_pipeline.event import Event
from .validator import validate_event
from .normalize import normalize_endpoint
from .ratelimit import RateLimiter

queue = BoundedQueue(max_size=100_000)
rate_limiter = RateLimiter(rate_per_sec=50_000)

class IngestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/events":
            self.send_response(404)
            self.end_headers()
            return

        if not rate_limiter.allow():
            self.send_response(429)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            return

        if not validate_event(data):
            self.send_response(400)
            self.end_headers()
            return

        event = Event(
            ts=data["ts"],
            service=data["service"],
            endpoint=normalize_endpoint(data["endpoint"]),
            status=data["status"],
            latency=data["latency_ms"],
        )

        if not queue.put(event):
            self.send_response(503)  # backpressure signal
            self.end_headers()
            return

        self.send_response(202)
        self.end_headers()

def run():
    server = HTTPServer(("0.0.0.0", 8000), IngestHandler)
    server.serve_forever()

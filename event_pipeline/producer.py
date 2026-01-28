import time
import random
from event_pipeline.event import Event

SERVICES = ["auth", "billing", "search"]
ENDPOINTS = ["/login", "/logout", "/pay", "/query"]

def generate_event():
    return Event(
        ts=time.time(),
        service=random.choice(SERVICES),
        endpoint=random.choice(ENDPOINTS),
        status=random.choice([200, 200, 200, 500]),
        latency=random.randint(10, 3000),
    )
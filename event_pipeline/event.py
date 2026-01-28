
class Event:
    __slots__ = ("ts", "service", "endpoint", "status", "latency")

    def __init__(self, ts, service, endpoint, status, latency):
        self.ts = ts
        self.service = service
        self.endpoint = endpoint
        self.status = status
        self.latency = latency

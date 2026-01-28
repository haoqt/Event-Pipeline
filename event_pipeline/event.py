
class Event:
    __slots__ = ("endpoint", "status", "latency", "priority")
    HIGH = 10
    LOW = 1

    def __init__(self, endpoint, status, latency):
        self.endpoint = endpoint
        self.status = status
        self.latency = latency
        self.priority = (
            self.HIGH if status >= 500 or latency > 1000 else self.LOW
        )

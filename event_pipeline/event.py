from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    ts: int
    service: str
    endpoint: str
    status: int
    latency_ms: int
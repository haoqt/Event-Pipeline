from event_pipeline.event import Event


class Ingestor:
    def __init__(self, metrics):
        self.metrics = metrics

    def parse(self, data: dict):
        try:
            event = Event(
                ts=int(data["ts"]),
                service=str(data["service"]),
                endpoint=self.normalize_endpoint(data["endpoint"]),
                status=int(data["status"]),
                latency_ms=int(data["latency_ms"]),
            )
            self.metrics.inc("ingest_ok")
            return event
        except Exception:
            self.metrics.inc("ingest_invalid")
            return None

    def normalize_endpoint(self, endpoint: str) -> str:
        return endpoint.split("?")[0]
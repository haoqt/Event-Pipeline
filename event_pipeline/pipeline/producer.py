import uuid
from datetime import datetime
from event_pipeline.models import Event


def produce(event_type: str, payload: dict) -> Event:
    return Event(
        id=str(uuid.uuid4()),
        type=event_type,
        payload=payload,
        created_at=datetime.utcnow(),
    )

from event_pipeline.models import Event
from event_pipeline.registry import registry


def reduce(event: Event):
    registry.add(event)

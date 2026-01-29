from event_pipeline.models import Event


def process(event: Event) -> Event:
    # place for validation, enrichment, filtering
    event.payload["processed"] = True
    return event

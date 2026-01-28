def validate_event(data: dict):
    try:
        return (
            isinstance(data["ts"], (int, float)) and
            isinstance(data["service"], str) and
            isinstance(data["endpoint"], str) and
            isinstance(data["status"], int) and
            isinstance(data["latency_ms"], int)
        )
    except KeyError:
        return False

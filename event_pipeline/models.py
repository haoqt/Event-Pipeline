from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass
class Event:
    id: str
    type: str
    payload: Dict[str, Any]
    created_at: datetime = datetime.utcnow()

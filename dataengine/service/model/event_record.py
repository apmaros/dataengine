import datetime
from dataclasses import dataclass


@dataclass
class EventRecord:
    start: datetime
    stop: datetime
    time: datetime
    description: str
    activity: str
    feel: int
    duration: int
    user_id: str

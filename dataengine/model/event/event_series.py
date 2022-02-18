import typing as t
from dataclasses import dataclass
from datetime import datetime


@dataclass
class EventSeries:
    index: t.List[datetime]
    body: t.List[str]
    duration: t.List[int]
    feel: t.List[str]

from dataclasses import dataclass
from datetime import datetime

from influxdb_client import Point

from dataengine.common.util import get_uuid


@dataclass
class Event:
    description: str
    activity: str
    time: datetime
    duration: int
    event_id: str = get_uuid()

    def as_point(self):
        return (Point('event')
                .tag('event_id', self.event_id)
                .field('description', self.description)
                .field('activity', self.activity)
                .field('time', self.time)
                .tag('duration', self.duration))

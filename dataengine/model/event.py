from dataclasses import dataclass
from datetime import datetime

from influxdb_client import Point

from dataengine.common.util import get_uuid

EVENT_MEASUREMENT_NAME = "events"


@dataclass
class Event:
    description: str
    activity: str
    feel: int
    time: datetime
    duration: int
    user_id: str
    event_id: str = get_uuid()

    def as_point(self):
        return (Point(EVENT_MEASUREMENT_NAME)
                .field('description', self.description)
                .tag('activity', self.activity)
                .tag('feel', self.feel)
                .time(self.time)
                .tag('duration', self.duration)
                .tag('user_id', self.user_id)
                .field('event_id', self.event_id))

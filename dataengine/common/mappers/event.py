import typing as t

from dataengine.model.dao.event import Event
from dataengine.model.event.event_series import EventSeries


def _events_to_series(events: t.List[Event]) -> EventSeries:
    return EventSeries(
        index=list(map(lambda e: e.time, events)),
        body=list(map(lambda e: e.body, events)),
        duration=list(map(lambda e: e.duration, events)),
        feel=list(map(lambda e: e.feel, events)),
    )

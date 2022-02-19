import typing as t

from dataengine.config import EVENT_NO_TIME_LABEL
from dataengine.model.dao.event import Event
from dataengine.model.item_group import ItemGroup


def group_events_by_date(events: t.List[Event]) -> t.Dict[str, Event]:
    grouped: t.Dict[str, ItemGroup] = {}

    for event in events:
        if event.time:
            key = event.time.strftime('%a, %d-%m-%Y')
        else:
            key = EVENT_NO_TIME_LABEL

        if key not in grouped:
            grouped[key] = ItemGroup(key, [])
        grouped[key].value.append(event)

    return grouped

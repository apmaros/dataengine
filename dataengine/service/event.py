import typing as t

from dataengine.model.dao.event import Event
from dataengine.model.item_group import ItemGroup


def group_events_by_date(events: t.List[Event]) -> t.Dict[str, Event]:
    grouped: t.Dict[str, ItemGroup] = {}

    for event in events:
        date = event.time.strftime('%a, %d-%m-%Y')
        if date not in grouped:
            grouped[date] = ItemGroup(date, [])
        grouped[date].value.append(event)

    return grouped

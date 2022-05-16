import datetime
import typing as t
from typing import Dict, Any

from dataengine.model.dao.event import Event
from dataengine.model.item_group import ItemGroup


def group_events_by_date(events: t.List[Event]) -> Dict[Any, ItemGroup]:
    grouped: t.Dict[t.Optional[datetime], ItemGroup] = {}

    for event in events:
        if event.time:
            key = event.time.date()
        else:
            key = None

        if key not in grouped:
            grouped[key] = ItemGroup(key, [])
        grouped[key].value.append(event)

    return grouped

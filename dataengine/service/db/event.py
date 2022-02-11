import typing
import uuid

from sqlalchemy import update, select, func, desc

from dataengine import Context
from dataengine.common.util import days_ago_datetime
from dataengine.model.dao.event import Event


def get_event(note_id):
    stmt = select(Event).filter(Event.id == note_id)

    with Context.db_session() as session:
        events = session.execute(stmt).scalars().all()

    return events[0] if events else None


def get_events_since(user_id, days_ago) -> typing.List[Event]:
    stmt = (select(Event)
            .filter(Event.user_id == user_id)
            .filter(Event.time > days_ago_datetime(days_ago))
            .order_by(desc(Event.time))
            )

    with Context.db_session() as session:
        events = session.execute(stmt).scalars().all()

    return events


def put_event(user_id: str, args: typing.Dict[str, str]):
    event = _args_to_event(user_id, args)

    with Context.db_session() as session:
        session.add(event)
        session.commit()


def update_event(user_id, args):
    event = _args_to_event(args, user_id)
    stmt = (update(Event)
        .where(Event.id == event.id)
        .values(
        user_id=event.user_id,
        body=event.body,
        activity=event.activity,
        duration=event.duration,
        time=event.time,
        feel=event.feel)
    )
    with Context.db_session() as session:
        session.execute(stmt)
        session.commit()


def _args_to_event(user_id, args) -> Event:
    event_id = args.get('id', uuid.uuid4())
    time = args.get('time')
    duration = args.get('duration')

    return Event(
        id=event_id,
        user_id=user_id,
        body=args['body'],
        activity=args.get('activity'),
        duration=duration if duration else None,
        time=time if time else func.now(),
        feel=args.get('feel'),
    )

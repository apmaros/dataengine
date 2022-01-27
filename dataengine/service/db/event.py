import typing

from sqlalchemy import func
from sqlalchemy import select

from dataengine import Context
from dataengine.common.util import days_ago_datetime
from dataengine.model.dao.event import Event


def get_events_since(user_id, days_ago) -> typing.List[Event]:
    statement = (select(Event)
                 .filter(Event.user_id == user_id)
                 .filter(Event.time > days_ago_datetime(days_ago))
                 )

    return Context.db_session().execute(statement).scalars().all()


def put_event(user_id: str, args: typing.Dict[str, str]):
    time = args.get('time')
    event = Event(
        user_id=user_id,
        body=args['body'],
        activity=args.get('activity'),
        duration=args.get('duration'),
        time=time if time else func.now(),
        feel=args.get('feel'),
    )
    session = Context.db_session()

    session.add(event)
    session.commit()

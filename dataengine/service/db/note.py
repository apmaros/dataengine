import typing

from sqlalchemy import select, desc, func

from dataengine import Context
from dataengine.common.util import days_ago_datetime
from dataengine.model.dao.note import Note


def get_notes_since(user_id, days_ago) -> typing.List[Note]:
    statement = (select(Note)
                 .filter(Note.user_id == user_id)
                 .filter(Note.created_at > days_ago_datetime(days_ago))
                 .order_by(desc(Note.created_at))
                 )

    with Context.db_session() as session:
        events = session.execute(statement).scalars().all()

    return events


def put_note(user_id: str, args: typing.Dict[str, str]):
    note = Note(
        user_id=user_id,
        body=args['body'],
        created_at=func.now(),
    )
    with Context.db_session() as session:
        session.add(note)
        session.commit()

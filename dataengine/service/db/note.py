import typing
import uuid

from sqlalchemy import select, desc, func

from dataengine import Context
from dataengine.common.util import days_ago_datetime
from dataengine.model.dao.note import Note
from dataengine.model.dao.note_with_sentiment import NoteWithSentiment
from dataengine.model.dao.sentiment import Sentiment


def get_notes_since(user_id, days_ago) -> typing.List[Note]:
    statement = (select(Note, Sentiment)
                 .filter(Note.user_id == user_id)
                 .filter(Note.created_at > days_ago_datetime(days_ago))
                 .join(Sentiment, Sentiment.parent_id == Note.id, isouter=True)
                 .order_by(desc(Note.created_at)))

    with Context.db_session() as session:
        notes = list(map(
            lambda r: NoteWithSentiment(r.Note, r.Sentiment),
            session.execute(statement)
        ))

    return notes


def put_note(user_id: str, args: typing.Dict[str, str]):
    note_id = uuid.uuid4()
    note = Note(
        id=note_id,
        user_id=user_id,
        body=args['body'],
        created_at=func.now(),
    )
    sentiment = Sentiment(
        id=uuid.uuid4(),
        user_id=user_id,
        parent_id=note_id,
        sad=args.get('sentiment_sad', None),
        anxiety=args.get('sentiment_anxiety', None),
        stress=args.get('sentiment_stress', None),
        happiness=args.get('sentiment_happiness', None),
        energy=args.get('sentiment_energy', None),
        creativity=args.get('sentiment_creativity', None),
    )
    with Context.db_session() as session:
        session.add(note)
        if not sentiment.blank():
            session.add(sentiment)
        session.commit()

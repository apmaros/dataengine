import typing as t
import uuid
from typing import List

from sqlalchemy import select, delete, desc, func

from dataengine import Context
from dataengine.common.util import days_ago_datetime
from dataengine.model.dao.geo_location import GeoLocation
from dataengine.model.dao.note import Note
from dataengine.model.dao.note_with_sentiment import NoteWithSentiment
from dataengine.model.dao.sentiment import Sentiment


def get_notes_since(user_id, days_ago) -> List[NoteWithSentiment]:
    statement = (select(Note, Sentiment, GeoLocation)
                 .filter(Note.user_id == user_id)
                 .filter(Note.created_at > days_ago_datetime(days_ago))
                 .join(Sentiment, Sentiment.parent_id == Note.id, isouter=True)
                 .join(GeoLocation, GeoLocation.parent_id == Note.id, isouter=True)
                 .order_by(desc(Note.created_at)))

    with Context.db_session() as session:
        notes = list(map(
            lambda r: NoteWithSentiment(r.Note, r.Sentiment, r.GeoLocation),
            session.execute(statement)
        ))

    return notes


def get_note(note_id):
    stmt = (select(Note, Sentiment, GeoLocation)
            .filter(Note.id == note_id)
            .join(Sentiment, Sentiment.parent_id == Note.id, isouter=True)
            .join(GeoLocation, GeoLocation.parent_id == Note.id, isouter=True))

    with Context.db_session() as session:
        notes = _build_notes_with_sentiment(session.execute(stmt))

    return notes[0] if notes else None


def put_note(user_id: str, args: t.Dict[str, str]):
    note_id = uuid.uuid4()
    note = args_to_node(args, note_id, user_id)
    sentiment = args_to_sentiment(args, note_id, user_id)
    location = args_to_location(args, note_id)

    with Context.db_session() as session:
        session.add(note)
        if not sentiment.blank():
            session.add(sentiment)
        if location:
            session.add(location)
        session.commit()


def args_to_location(args, note_id) -> t.Optional[GeoLocation]:
    name = args.get('geo-name', None)
    lat = args.get('geo-lat', None)
    lng = args.get('geo-lng', None)

    if not all([lat, lng]):
        return None

    loc = GeoLocation()
    loc.parent_id = note_id
    loc.name = name
    loc.lat = lat
    loc.lng = lng

    return loc


def update_note(_):
    raise 'UNIMPLEMENTED'


def delete_note(note_id: str):
    with Context.db_session() as session:
        session.execute(delete(Note).where(Note.id == note_id))
        session.execute(delete(Sentiment).where(Sentiment.parent_id == note_id))
        session.commit()


def args_to_node(args, note_id, user_id):
    return Note(
        id=note_id,
        user_id=user_id,
        body=args['body'],
        created_at=func.now(),
    )


def args_to_sentiment(args, note_id, user_id):
    return Sentiment(
        id=uuid.uuid4(),
        user_id=user_id,
        parent_id=note_id,
        sad=_get_int(args, 'sentiment_sad'),
        anxiety=_get_int(args, 'sentiment_anxiety'),
        stress=_get_int(args, 'sentiment_stress'),
        happiness=_get_int(args, 'sentiment_happiness'),
        energy=_get_int(args, 'sentiment_energy'),
        creativity=_get_int(args, 'sentiment_creativity'),
    )


def _get_int(args, key):
    val = args.get(key, None)
    return int(val) if val else None


def _build_notes_with_sentiment(rows):
    return list(map(
        lambda r: NoteWithSentiment(r.Note, r.Sentiment, r.GeoLocation),
        rows
    ))

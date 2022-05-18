from dataclasses import dataclass

from dataengine.model.dao.geo_location import GeoLocation
from dataengine.model.dao.note import Note
from dataengine.model.dao.sentiment import Sentiment


@dataclass
class NoteWithSentiment:
    note: Note
    sentiment: Sentiment
    geo_location: GeoLocation

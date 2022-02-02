from dataclasses import dataclass

from dataengine.model.dao.note import Note
from dataengine.model.dao.sentiment import Sentiment


@dataclass
class NoteWithSentiment:
    note: Note
    sentiment: Sentiment

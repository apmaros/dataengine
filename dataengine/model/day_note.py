from dataclasses import dataclass

from influxdb_client import Point

from dataengine.common.util import get_uuid

DAY_NOTE_MEASURE_NAME = "day_notes"


@dataclass
class DayNote:
    note: str
    sad: int
    energetic: int
    anxious: int
    creative: int
    user_id: str
    day_note_id: str = get_uuid()


def day_note_to_record(day_note: DayNote):
    return (Point(DAY_NOTE_MEASURE_NAME)
            .field('note', day_note.note)
            .tag('sad', day_note.sad)
            .tag('energetic', day_note.energetic)
            .tag('anxious', day_note.anxious)
            .tag('creative', day_note.creative)
            .field('user_id', day_note.user_id)
            .field('day_note_id', day_note.day_note_id))

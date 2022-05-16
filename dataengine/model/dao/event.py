from sqlalchemy import Column, String, DATETIME, SMALLINT, Unicode, TIMESTAMP

from dataengine.model.dao.base import Base


class Event(Base):
    __tablename__ = "event"

    user_id = Column(String)
    body = Column(Unicode)
    activity = Column(String)
    duration = Column(SMALLINT)
    time = Column(DATETIME)
    feel = Column(SMALLINT)
    created_at = Column(TIMESTAMP)

    def __repr__(self):
        return (f'user_id={self.user_id},'
                f' time={self.time},'
                f' activity={self.activity},'
                f' body={self.body}')

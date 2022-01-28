from sqlalchemy import Column, String, DATETIME, SMALLINT, Unicode, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

from dataengine.model.dao.base import Base

Base = declarative_base(cls=Base)


class Event(Base):
    __tablename__ = "event"

    user_id = Column(String)
    body = Column(Unicode)
    activity = Column(String)
    duration = Column(SMALLINT)
    time = Column(DATETIME)
    feel = Column(SMALLINT)
    created_at = Column(TIMESTAMP)

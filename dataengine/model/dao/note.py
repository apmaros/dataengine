from sqlalchemy import Column, String, Unicode, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

from dataengine.model.dao.base import Base

Base = declarative_base(cls=Base)


class Note(Base):
    __tablename__ = "note"

    user_id = Column(String)
    body = Column(Unicode)
    created_at = Column(TIMESTAMP)

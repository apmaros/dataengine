from sqlalchemy import Column, String, Unicode, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID

from dataengine.model.dao.base import Base


class Note(Base):
    __tablename__ = "note"
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(String)
    body = Column(Unicode)
    created_at = Column(TIMESTAMP)

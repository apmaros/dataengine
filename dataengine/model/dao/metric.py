from sqlalchemy import Column, String, DATETIME, INTEGER, TIMESTAMP

from dataengine.model.dao.base import Base


class Metric(Base):
    __tablename__ = "event"

    name = Column(String)
    value = Column(INTEGER)
    time = Column(DATETIME)
    created_at = Column(TIMESTAMP)

from sqlalchemy import Column, String, DATETIME, INTEGER

from dataengine.model.dao.base import Base


class Metric(Base):
    __tablename__ = "metric"
    user_id = Column(String)
    name = Column(String)
    value = Column(INTEGER)
    event = Column(String)
    time = Column(DATETIME)

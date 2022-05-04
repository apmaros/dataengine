from sqlalchemy import Column, String, Text, TIMESTAMP

from dataengine.model.dao.base import Base


class UserMetric(Base):
    __tablename__ = "user_metric"
    user_id = Column(String)
    name = Column(String)
    description = Column(Text)
    created_at = Column(TIMESTAMP)

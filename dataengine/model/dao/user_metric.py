from sqlalchemy import Column, String, Text

from dataengine.model.dao.base import Base


class Metric(Base):
    __tablename__ = "user_metric"
    user_id = Column(String)
    metric_id = Column(String)
    name = Column(String)
    description = Column(Text)

from sqlalchemy import Column, String, SMALLINT

from dataengine.model.dao.base import Base


class HeartPressureReading(Base):
    __tablename__ = "heart_pressure_reading"

    user_id = Column(String)
    systolic = Column(SMALLINT)
    diastolic = Column(SMALLINT)
    heart_rate = Column(SMALLINT)
    last_activity = Column(String)

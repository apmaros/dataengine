from sqlalchemy import Column, String, SMALLINT
from sqlalchemy.dialects.postgresql import UUID

from dataengine.model.dao.base import Base


class Sentiment(Base):
    __tablename__ = "sentiment"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(String)
    parent_id = Column(String)
    sad = Column(SMALLINT)
    anxiety = Column(SMALLINT)
    stress = Column(SMALLINT)
    happiness = Column(SMALLINT)
    energy = Column(SMALLINT)
    creativity = Column(SMALLINT)

    def blank(self):
        return not any([
            self.sad,
            self.anxiety,
            self.stress,
            self.happiness,
            self.energy,
            self.creativity
        ])

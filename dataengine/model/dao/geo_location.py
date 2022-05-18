from sqlalchemy import Column, String, Float

from dataengine.model.dao.base import Base


class GeoLocation(Base):
    __tablename__ = "geo_location"

    parent_id = Column(String)
    lng = Column(Float)
    lat = Column(Float)
    name = Column(String)

    def __repr__(self):
        return (f'parent_id={self.parent_id},'
                f' lng={self.lng},'
                f' lat={self.lat}'
                f' name={self.name}')

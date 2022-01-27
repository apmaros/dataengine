from sqlalchemy import Column, TIMESTAMP
from sqlalchemy.ext.declarative import declared_attr

from dataengine.model.dao.default_columns import id_uuid


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = id_uuid
    created_at = Column(TIMESTAMP)

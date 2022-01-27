import string
import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

id_uuid = Column(
    UUID(as_uuid=True),
    primary_key=True,
    default=uuid.uuid4,
    unique=True,
    nullable=False,
)


def make_id_fk(field: string = 'user.id') -> Column:
    return Column(
        ForeignKey(field),
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

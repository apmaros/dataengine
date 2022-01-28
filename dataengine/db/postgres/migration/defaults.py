import uuid

from sqlalchemy import Column, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID


def make_id_uuid(column_name: str, is_unique=True) -> Column:
    return Column(
        column_name,
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=is_unique,
        nullable=False
    )


def make_created_at_column() -> Column:
    return Column('created_at', TIMESTAMP, server_default=func.now())

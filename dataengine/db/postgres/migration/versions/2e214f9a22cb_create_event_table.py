"""create event table

Revision ID: 2e214f9a22cb
Revises:
Create Date: 2022-01-27 14:26:19.435415+00:00

"""
import uuid

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '2e214f9a22cb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('event',
                    sa.Column(
                        'id',
                        UUID(as_uuid=True),
                        primary_key=True,
                        default=uuid.uuid4,
                        unique=True,
                        nullable=False
                    ),
                    sa.Column('body', sa.Unicode(500), nullable=False),
                    sa.Column('time', sa.DateTime(), nullable=False),
                    sa.Column('feel', sa.SMALLINT(), nullable=True),
                    sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now()),
                    )


def downgrade():
    pass

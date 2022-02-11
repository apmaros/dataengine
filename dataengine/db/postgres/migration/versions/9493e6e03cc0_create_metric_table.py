"""create metric table

Revision ID: 9493e6e03cc0
Revises: 90cc8c271744
Create Date: 2022-02-11 13:38:41.960218+00:00

"""
import uuid

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '9493e6e03cc0'
down_revision = '90cc8c271744'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('metric',
                    sa.Column(
                        'id',
                        UUID(as_uuid=True),
                        primary_key=True,
                        default=uuid.uuid4,
                        unique=True,
                        nullable=False
                    ),
                    sa.Column('name', sa.String(50), nullable=False),
                    sa.Column('value', sa.INTEGER, nullable=True),
                    sa.Column('time', sa.TIMESTAMP, server_default=sa.func.now()),
                    sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now()),
                    )


def downgrade():
    op.drop_table('metric')

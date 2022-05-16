"""add user_metric_id to metric

Revision ID: f16eac25075b
Revises: 500652d0abb8
Create Date: 2022-05-04 16:56:54.532809+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f16eac25075b'
down_revision = '500652d0abb8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'metric',
        sa.Column('user_metric_id', sa.String(50), nullable=True)
    )


def downgrade():
    pass

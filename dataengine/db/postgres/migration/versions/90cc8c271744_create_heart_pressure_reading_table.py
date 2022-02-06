"""create heart_pressure table

Revision ID: 90cc8c271744
Revises: e9f97b6e35d1
Create Date: 2022-02-06 14:24:57.936834+00:00

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
from db.postgres.migration.defaults import make_id_uuid, make_created_at_column

revision = '90cc8c271744'
down_revision = 'e9f97b6e35d1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'heart_pressure_reading',
        make_id_uuid('id'),
        sa.Column('user_id', sa.String(50), nullable=False),
        sa.Column('systolic', sa.SMALLINT(), nullable=True),
        sa.Column('diastolic', sa.SMALLINT(), nullable=True),
        sa.Column('heart_rate', sa.SMALLINT(), nullable=True),
        sa.Column('last_activity', sa.String(300), nullable=False),
        make_created_at_column()
    )


def downgrade():
    op.drop_table('heart_pressure_reading')

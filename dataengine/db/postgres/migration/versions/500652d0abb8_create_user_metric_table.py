"""create user metric table

Revision ID: 500652d0abb8
Revises: 9493e6e03cc0
Create Date: 2022-05-02 19:30:57.833433+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from dataengine.db.postgres.migration.defaults import make_id_uuid, \
    make_created_at_column

revision = '500652d0abb8'
down_revision = '9493e6e03cc0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user_metric',
        make_id_uuid('id'),
        sa.Column('user_id', sa.String(50), nullable=False),
        make_created_at_column(),
        # values
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
    )


def downgrade():
    op.drop_table('user_metric')

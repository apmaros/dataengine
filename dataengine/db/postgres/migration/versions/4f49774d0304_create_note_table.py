"""create note table

Revision ID: 4f49774d0304
Revises: 2e214f9a22cb
Create Date: 2022-01-28 09:09:47.933870+00:00

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
from dataengine.db.postgres.migration.defaults import make_id_uuid, make_created_at_column

revision = '4f49774d0304'
down_revision = '2e214f9a22cb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'note',
        make_id_uuid('id'),
        sa.Column('user_id', sa.String(50), nullable=False),
        sa.Column('body', sa.Unicode(5000), nullable=False),
        make_created_at_column()
    )


def downgrade():
    op.drop_table('note')

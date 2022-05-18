"""create table geo_location

Revision ID: 0c0d6eed53ad
Revises: f16eac25075b
Create Date: 2022-05-18 01:15:02.514389+00:00

"""

from alembic import op
import sqlalchemy as sa

from dataengine.db.postgres.migration.defaults import make_created_at_column, \
    make_id_uuid

revision = '0c0d6eed53ad'
down_revision = 'f16eac25075b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('geo_location',
                    make_id_uuid('id'),
                    sa.Column('lng', sa.FLOAT),
                    sa.Column('lat', sa.FLOAT),
                    make_id_uuid('parent_id', is_unique=False, nullable=False),
                    sa.Column('name', sa.String(50), nullable=False),
                    make_created_at_column()
                    )


def downgrade():
    op.drop_table('geo_location')

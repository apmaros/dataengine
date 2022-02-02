"""create sentiment table

Revision ID: e9f97b6e35d1
Revises: 4f49774d0304
Create Date: 2022-02-01 17:55:25.479906+00:00

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
from dataengine.db.postgres.migration.defaults import make_id_uuid, make_created_at_column

revision = 'e9f97b6e35d1'
down_revision = '4f49774d0304'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'sentiment',
        # header
        make_id_uuid('id'),
        sa.Column('user_id', sa.String(50), nullable=False),
        make_id_uuid('parent_id', is_unique=False, nullable=True),
        make_created_at_column(),
        # values
        sa.Column('sad', sa.SmallInteger, nullable=True),
        sa.Column('anxiety', sa.SmallInteger, nullable=True),
        sa.Column('stress', sa.SmallInteger, nullable=True),
        sa.Column('happiness', sa.SmallInteger, nullable=True),
        sa.Column('energy', sa.SmallInteger, nullable=True),
        sa.Column('creativity', sa.SmallInteger, nullable=True),
    )


def downgrade():
    op.drop_table('projects')

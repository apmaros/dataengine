"""create metric table

Revision ID: 9493e6e03cc0
Revises: 90cc8c271744
Create Date: 2022-02-11 13:38:41.960218+00:00

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
from dataengine.db.postgres.migration.defaults import make_id_uuid, make_created_at_column

revision = '9493e6e03cc0'
down_revision = '90cc8c271744'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('metric',
                    make_id_uuid('id'),
                    sa.Column('user_id', sa.String(50), nullable=False),
                    sa.Column('name', sa.String(50), nullable=False),
                    sa.Column('event', sa.String(250), nullable=False),
                    sa.Column('value', sa.INTEGER, nullable=True),
                    sa.Column('time', sa.TIMESTAMP, server_default=sa.func.now()),
                    make_created_at_column(),
                    )


def downgrade():
    op.drop_table('metric')

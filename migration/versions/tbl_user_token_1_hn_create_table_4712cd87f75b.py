"""tbl_user_token 1 hn create table

Revision ID: 4712cd87f75b
Revises: 2c6d7f9d1158
Create Date: 2015-11-13 08:20:22.862593

"""

# revision identifiers, used by Alembic.
revision = '4712cd87f75b'
down_revision = '2c6d7f9d1158'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('tbl_user_token',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('tbl_user.id', ondelete='CASCADE', onupdate='CASCADE')),
        sa.Column('device_id', sa.String),
        sa.Column('device_type', sa.String),
        sa.Column('device_token', sa.String),
        sa.Column('access_token', sa.String),
        sa.Column('is_active', sa.Boolean),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade():
    op.drop_table('tbl_user_token')

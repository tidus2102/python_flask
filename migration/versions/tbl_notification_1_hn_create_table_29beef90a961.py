"""tbl_notification 1 hn create table

Revision ID: 29beef90a961
Revises: 4b1916f01ae
Create Date: 2015-11-13 08:40:03.370003

"""

# revision identifiers, used by Alembic.
revision = '29beef90a961'
down_revision = '4b1916f01ae'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('tbl_notification',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('tbl_user.id', ondelete='CASCADE', onupdate='CASCADE')),
        sa.Column('activity_id', sa.Integer, sa.ForeignKey('tbl_activity.id', ondelete='CASCADE', onupdate='CASCADE')),
        sa.Column('is_read', sa.Boolean),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade():
    op.drop_table('tbl_notification')

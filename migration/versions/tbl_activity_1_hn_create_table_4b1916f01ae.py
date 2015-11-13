"""tbl_activity 1 hn create table

Revision ID: 4b1916f01ae
Revises: 38dc12f92ed3
Create Date: 2015-11-13 08:39:55.457703

"""

# revision identifiers, used by Alembic.
revision = '4b1916f01ae'
down_revision = '38dc12f92ed3'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('tbl_activity',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('tbl_user.id', ondelete='CASCADE', onupdate='CASCADE')),
        sa.Column('action', sa.String),
        sa.Column('model_name', sa.String),
        sa.Column('model_id', sa.Integer),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade():
    op.drop_table('tbl_activity')
"""tbl_user 2 hn add column role

Revision ID: 23e884e94f4b
Revises: 29beef90a961
Create Date: 2015-11-13 09:45:52.729777

"""

# revision identifiers, used by Alembic.
revision = '23e884e94f4b'
down_revision = '29beef90a961'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'tbl_user',
        sa.Column('role', sa.String)
    )


def downgrade():
    op.drop_column('tbl_user', 'role')

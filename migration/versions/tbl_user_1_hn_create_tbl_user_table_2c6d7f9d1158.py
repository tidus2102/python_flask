"""tbl_user 1 hn create tbl_user table

Revision ID: 2c6d7f9d1158
Revises: 
Create Date: 2015-11-11 11:35:02.956724

"""

# revision identifiers, used by Alembic.
revision = '2c6d7f9d1158'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('tbl_user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('first_name', sa.String),
        sa.Column('last_name', sa.String),
        sa.Column('full_name', sa.String),
        sa.Column('username', sa.String),
        sa.Column('email', sa.String),
        sa.Column('password', sa.String),
        sa.Column('secret_token', sa.String),
        sa.Column('status', sa.String),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade():
    op.drop_table('tbl_user')

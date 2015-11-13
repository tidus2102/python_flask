"""tbl_email 1 hn create table

Revision ID: 38dc12f92ed3
Revises: 4712cd87f75b
Create Date: 2015-11-13 08:28:40.821011

"""

# revision identifiers, used by Alembic.
revision = '38dc12f92ed3'
down_revision = '4712cd87f75b'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('tbl_email',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('subject', sa.String),
        sa.Column('content', sa.String),
        sa.Column('sender_name', sa.String),
        sa.Column('sender_email', sa.String),
        sa.Column('receiver_emails', sa.String),
        sa.Column('type', sa.String),
        sa.Column('status', sa.String),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade():
    op.drop_table('tbl_email')

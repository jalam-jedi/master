"""ADDED ADMIN COLUMN

Revision ID: 00cd5f454ae3
Revises: 7360186eb77b
Create Date: 2025-01-17 01:04:15.462628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00cd5f454ae3'
down_revision = '7360186eb77b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_admin', sa.Boolean(), nullable=False,server_default=sa.text('0')))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('is_admin')

    # ### end Alembic commands ###

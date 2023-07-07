"""empty message

Revision ID: 79a4ff0653c7
Revises: 0eb9ef997079
Create Date: 2023-07-06 11:20:16.856017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79a4ff0653c7'
down_revision = '0eb9ef997079'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('participants', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'event', ['event_name'], ['event_name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('participants', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('id')

    # ### end Alembic commands ###

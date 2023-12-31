"""empty message

Revision ID: da2dfc18c41c
Revises: 7de997ac9f0b
Create Date: 2023-09-07 22:38:06.653791

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da2dfc18c41c'
down_revision = '7de997ac9f0b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('winers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('marks', sa.Integer(), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('winers')
        batch_op.drop_column('event_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('winers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('event_name', sa.VARCHAR(length=100), nullable=False))
        batch_op.add_column(sa.Column('winers', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key(None, 'event', ['event_name'], ['event_name'])
        batch_op.drop_column('marks')

    # ### end Alembic commands ###

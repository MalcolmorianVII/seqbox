"""empty message

Revision ID: c7db23d26c06
Revises: ecc27c395564
Create Date: 2022-07-07 12:35:48.259660

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7db23d26c06'
down_revision = 'ecc27c395564'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sample', sa.Column('date_collected', sa.DateTime(), nullable=True))
    op.add_column('sample', sa.Column('date_received', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sample', 'date_received')
    op.drop_column('sample', 'date_collected')
    # ### end Alembic commands ###

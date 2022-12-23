"""empty message

Revision ID: 860aee337f99
Revises: 48b8b0ec30f2
Create Date: 2022-12-23 08:21:13.330606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '860aee337f99'
down_revision = '48b8b0ec30f2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('raw_sequencing_batch', 'library_prep_method')
    op.add_column('raw_sequencing_illumina', sa.Column('library_prep_method', sa.VARCHAR(length=64), nullable=True))
    op.add_column('raw_sequencing_nanopore', sa.Column('library_prep_method', sa.VARCHAR(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('raw_sequencing_nanopore', 'library_prep_method')
    op.drop_column('raw_sequencing_illumina', 'library_prep_method')
    op.add_column('raw_sequencing_batch', sa.Column('library_prep_method', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    # ### end Alembic commands ###

"""Added is_validated

Revision ID: bde0dae657dc
Revises: 3fed78a29305
Create Date: 2024-08-16 10:32:06.489840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bde0dae657dc'
down_revision = '3fed78a29305'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('is_validated', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('categories', 'is_validated')
    # ### end Alembic commands ###

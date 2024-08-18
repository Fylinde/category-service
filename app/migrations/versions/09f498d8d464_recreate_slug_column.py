"""Recreate slug column

Revision ID: 09f498d8d464
Revises: c6d541628cb5
Create Date: 2024-08-16 07:37:22.773029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09f498d8d464'
down_revision = 'c6d541628cb5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_categories_name', table_name='categories')
    op.drop_constraint('uq_categories_slug', 'categories', type_='unique')
    op.create_index(op.f('ix_categories_slug'), 'categories', ['slug'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_categories_slug'), table_name='categories')
    op.create_unique_constraint('uq_categories_slug', 'categories', ['slug'])
    op.create_index('ix_categories_name', 'categories', ['name'], unique=False)
    # ### end Alembic commands ###

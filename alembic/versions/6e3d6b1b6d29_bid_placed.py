"""bid placed

Revision ID: 6e3d6b1b6d29
Revises: b43db533e969
Create Date: 2022-04-29 12:04:33.207033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e3d6b1b6d29'
down_revision = 'b43db533e969'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bidding', sa.Column('bid_placed_date', sa.DateTime(), nullable=True))
    op.drop_column('bidding', 'bid_expire_date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bidding', sa.Column('bid_expire_date', sa.DATETIME(), nullable=False))
    op.drop_column('bidding', 'bid_placed_date')
    # ### end Alembic commands ###
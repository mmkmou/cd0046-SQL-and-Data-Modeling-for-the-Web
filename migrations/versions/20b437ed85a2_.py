"""empty message

Revision ID: 20b437ed85a2
Revises: 24784d4e37c2
Create Date: 2022-05-06 21:07:10.821113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20b437ed85a2'
down_revision = '24784d4e37c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'Show', ['artist_id', 'venue_id', 'start_time'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Show', type_='unique')
    # ### end Alembic commands ###

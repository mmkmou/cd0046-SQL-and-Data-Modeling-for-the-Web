"""empty message

Revision ID: 308f7f4d05aa
Revises: 8e0a48b88a4f
Create Date: 2022-05-07 02:44:30.693041

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '308f7f4d05aa'
down_revision = '8e0a48b88a4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Artist', 'state',
               existing_type=postgresql.ENUM('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', name='state'),
               nullable=False)
    op.alter_column('Artist', 'genres',
               existing_type=postgresql.ARRAY(postgresql.ENUM('alternative', 'Blues', 'Classical', 'Country', 'Electronic', 'Folk', 'Funk', 'HipHop', 'HeavyMetal', 'Instrumental', 'Jazz', 'MusicalTheatre', 'Pop', 'Punk', 'RnB', 'Reggae', 'RocknRoll', 'Soul', 'Other', name='genre')),
               nullable=False)
    op.alter_column('Venue', 'state',
               existing_type=postgresql.ENUM('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', name='state'),
               nullable=False)
    op.alter_column('Venue', 'genres',
               existing_type=postgresql.ARRAY(postgresql.ENUM('alternative', 'Blues', 'Classical', 'Country', 'Electronic', 'Folk', 'Funk', 'HipHop', 'HeavyMetal', 'Instrumental', 'Jazz', 'MusicalTheatre', 'Pop', 'Punk', 'RnB', 'Reggae', 'RocknRoll', 'Soul', 'Other', name='genre')),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'genres',
               existing_type=postgresql.ARRAY(postgresql.ENUM('alternative', 'Blues', 'Classical', 'Country', 'Electronic', 'Folk', 'Funk', 'HipHop', 'HeavyMetal', 'Instrumental', 'Jazz', 'MusicalTheatre', 'Pop', 'Punk', 'RnB', 'Reggae', 'RocknRoll', 'Soul', 'Other', name='genre')),
               nullable=True)
    op.alter_column('Venue', 'state',
               existing_type=postgresql.ENUM('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', name='state'),
               nullable=True)
    op.alter_column('Artist', 'genres',
               existing_type=postgresql.ARRAY(postgresql.ENUM('alternative', 'Blues', 'Classical', 'Country', 'Electronic', 'Folk', 'Funk', 'HipHop', 'HeavyMetal', 'Instrumental', 'Jazz', 'MusicalTheatre', 'Pop', 'Punk', 'RnB', 'Reggae', 'RocknRoll', 'Soul', 'Other', name='genre')),
               nullable=True)
    op.alter_column('Artist', 'state',
               existing_type=postgresql.ENUM('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', name='state'),
               nullable=True)
    # ### end Alembic commands ###

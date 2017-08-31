"""empty message

Revision ID: 7e78dfccfde1
Revises: 
Create Date: 2017-08-29 17:29:53.116373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e78dfccfde1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('max_wave_height', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'max_wave_height')
    # ### end Alembic commands ###

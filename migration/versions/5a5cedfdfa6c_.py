"""empty message

Revision ID: 5a5cedfdfa6c
Revises: 58737ff6f2d3
Create Date: 2024-09-22 00:52:32.419968

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '5a5cedfdfa6c'
down_revision: Union[str, None] = '58737ff6f2d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Matches', sa.Column('player1_id', sa.Integer(), nullable=True))
    op.add_column('Matches', sa.Column('player2_id', sa.Integer(), nullable=True))
    op.drop_constraint('Matches_player1_fkey', 'Matches', type_='foreignkey')
    op.drop_constraint('Matches_player2_fkey', 'Matches', type_='foreignkey')
    op.create_foreign_key(None, 'Matches', 'Players', ['player1_id'], ['id'])
    op.create_foreign_key(None, 'Matches', 'Players', ['player2_id'], ['id'])
    op.drop_column('Matches', 'player1')
    op.drop_column('Matches', 'player2')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Matches', sa.Column('player2', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('Matches', sa.Column('player1', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'Matches', type_='foreignkey')
    op.drop_constraint(None, 'Matches', type_='foreignkey')
    op.create_foreign_key('Matches_player2_fkey', 'Matches', 'Players', ['player2'], ['id'])
    op.create_foreign_key('Matches_player1_fkey', 'Matches', 'Players', ['player1'], ['id'])
    op.drop_column('Matches', 'player2_id')
    op.drop_column('Matches', 'player1_id')
    # ### end Alembic commands ###

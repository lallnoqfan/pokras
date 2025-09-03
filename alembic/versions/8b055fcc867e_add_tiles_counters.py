"""add tiles counters

Revision ID: 8b055fcc867e
Revises: 74e3315ba15f
Create Date: 2025-09-01 16:12:42.029150

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from modules.game.models.choices.game_map import GameMap

# revision identifiers, used by Alembic.
revision: str = '8b055fcc867e'
down_revision: Union[str, Sequence[str], None] = '74e3315ba15f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ## game ##
    with op.batch_alter_table('game', schema=None) as batch_op:
        # batch_op.add_column(sa.Column('tiles_num', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('neutral_tiles_num', sa.Integer(), nullable=True))

    # op.execute(f"UPDATE game SET tiles_num = {234} WHERE map IS '{GameMap.eu_classic}'")
    # op.execute(f"UPDATE game SET tiles_num = {180} WHERE map IS '{GameMap.stalker}'")
    # op.execute(f"UPDATE game SET tiles_num = {95} WHERE map IS '{GameMap.korea}'")
    # op.execute(f"UPDATE game SET tiles_num = {86} WHERE map IS '{GameMap.ops_ass}'")

    op.execute(f"""
                UPDATE game SET neutral_tiles_num = (
                    SELECT game.tiles_num - COUNT(*)
                    FROM tile WHERE tile.game_id = game.id AND tile.owner_id IS NOT NULL
                )
                """)
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.alter_column('tiles_num', nullable=False)

    # ## country ##
    with op.batch_alter_table('country', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tiles_num', sa.Integer(), nullable=True))

    op.execute(f"UPDATE country SET tiles_num = (SELECT COUNT(*) FROM tile WHERE tile.owner_id = country.id)")

    with op.batch_alter_table('country', schema=None) as batch_op:
        batch_op.alter_column('tiles_num', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.drop_column('tiles_num')
        batch_op.drop_column('neutral_tiles_num')

    with op.batch_alter_table('country', schema=None) as batch_op:
        batch_op.drop_column('tiles_num')

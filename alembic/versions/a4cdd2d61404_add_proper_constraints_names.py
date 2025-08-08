"""add proper constraints names

Revision ID: a4cdd2d61404
Revises: 0c96b40927f9
Create Date: 2025-08-08 13:44:03.971218

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4cdd2d61404'
down_revision: Union[str, Sequence[str], None] = '0c96b40927f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.create_primary_key(batch_op.f('pk_game_id'), ['id'])

    with op.batch_alter_table('country', schema=None) as batch_op:
        batch_op.create_primary_key(batch_op.f('pk_country_id'), ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_country_game_id_game_id'), 'game', ['game_id'], ['id'], ondelete='CASCADE')
        batch_op.create_unique_constraint(batch_op.f('uq_country_color'), ['color'])
        batch_op.create_unique_constraint(batch_op.f('uq_country_name'), ['name'])

    with op.batch_alter_table('country', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_country_game_id_game_id'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('uq_country_color'), type_='unique')
        batch_op.drop_constraint(batch_op.f('uq_country_name'), type_='unique')

    with op.batch_alter_table('country', schema=None) as batch_op:
        batch_op.create_foreign_key(batch_op.f('fk_country_game_id_game_id'), 'game', ['game_id'], ['id'], ondelete='CASCADE')
        batch_op.create_unique_constraint(batch_op.f('uq_country_color'), ['color'])
        batch_op.create_unique_constraint(batch_op.f('uq_country_name'), ['name'])

    with op.batch_alter_table('tile', schema=None) as batch_op:
        batch_op.create_primary_key(batch_op.f('pk_tile_id'), ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_tile_game_id_game_id'), 'game', ['game_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(batch_op.f('fk_tile_owner_id_country_id'), 'country', ['owner_id'], ['id'], ondelete='CASCADE')
        batch_op.create_unique_constraint(batch_op.f('uq_tile_code'), ['code'])

    with op.batch_alter_table('tile', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_tile_game_id_game_id'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_tile_owner_id_country_id'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('uq_tile_code'), type_='unique')

    with op.batch_alter_table('tile', schema=None) as batch_op:
        batch_op.create_foreign_key(batch_op.f('fk_tile_game_id_game_id'), 'game', ['game_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(batch_op.f('fk_tile_owner_id_country_id'), 'country', ['owner_id'], ['id'], ondelete='CASCADE')
        batch_op.create_unique_constraint(batch_op.f('uq_tile_code'), ['code'])


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('country', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_country_game_id_game_id'), type_='foreignkey')

    with op.batch_alter_table('country', schema=None) as batch_op:
        batch_op.create_foreign_key(batch_op.f('fk_country_game_id_game_id'), 'game', ['game_id'], ['id'])

    with op.batch_alter_table('tile', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_tile_game_id_game_id'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_tile_owner_id_country_id'), type_='foreignkey')

    with op.batch_alter_table('tile', schema=None) as batch_op:
        batch_op.create_foreign_key(batch_op.f('fk_tile_game_id_game_id'), 'game', ['game_id'], ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_tile_owner_id_country_id'), 'country', ['owner_id'], ['id'])

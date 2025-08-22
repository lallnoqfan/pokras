"""fix roll values

Revision ID: da482cfe40db
Revises: 580cb9a66459
Create Date: 2025-08-22 17:36:17.809575

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from db.engine import Session

# revision identifiers, used by Alembic.
revision: str = 'da482cfe40db'
down_revision: Union[str, Sequence[str], None] = '580cb9a66459'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    session = Session(bind=bind)

    games = session.query(sa.Table('game', sa.MetaData(), autoload_with=bind)).all()

    for game in games:
        roll_list = game.roll_values.replace("|", ",").split(",")
        if len(roll_list) == 20:
            continue
        op.execute(f"UPDATE game SET roll_values = '1,1,1,1,1,1,1,1,1,1|3,5,9,15|4,7,7|2,3,5' WHERE id = {game.id}")

    session.close()


def downgrade() -> None:
    """Downgrade schema."""
    pass

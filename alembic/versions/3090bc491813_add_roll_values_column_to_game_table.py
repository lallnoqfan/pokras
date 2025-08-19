"""Add roll values column to game table

Revision ID: 3090bc491813
Revises: 498df4b1b6c3
Create Date: 2025-08-18 21:48:16.111411

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3090bc491813'
down_revision: Union[str, Sequence[str], None] = '498df4b1b6c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('game', sa.Column('roll_values', sa.String(length=100), nullable=False,
                                    server_default="1,1,1,1,1,1,1,1,1,1|3,5,9,15|4,7,7|2,3,5"))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('game', 'roll_values')

"""rename player to country

Revision ID: 5d4af7ff9fb2
Revises: a7e2c236bde0
Create Date: 2025-08-04 23:49:01.013626

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '5d4af7ff9fb2'
down_revision: Union[str, Sequence[str], None] = 'a7e2c236bde0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table('player', 'country')


def downgrade() -> None:
    """Downgrade schema."""
    op.rename_table('country', 'player')

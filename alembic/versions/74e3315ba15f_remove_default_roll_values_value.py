"""remove default 'roll_values' value

Revision ID: 74e3315ba15f
Revises: da482cfe40db
Create Date: 2025-08-22 17:59:13.884172

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74e3315ba15f'
down_revision: Union[str, Sequence[str], None] = 'da482cfe40db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.alter_column('roll_values', server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.alter_column('roll_values', server_default="1,1,1,1,1,1,1,1,1,1|3,5,9,15|4,7,7|2,3,5")

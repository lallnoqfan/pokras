"""add game map column

Revision ID: 0144257ae6b2
Revises: cbb7fc8f8e30
Create Date: 2025-08-11 02:39:27.012326

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0144257ae6b2'
down_revision: Union[str, Sequence[str], None] = 'cbb7fc8f8e30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('map', sa.Enum("eu_classic", "stalker", native_enum=False), nullable=True))

    op.execute("UPDATE game SET map = 'eu_classic' WHERE map IS NULL")

    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.alter_column('map', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.drop_column('map')

"""game cooldown fields

Revision ID: 73493bb59056
Revises: 3a1a3d2aee04
Create Date: 2025-08-19 15:43:19.229012

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73493bb59056'
down_revision: Union[str, Sequence[str], None] = '3a1a3d2aee04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('use_cooldown', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('cooldown', sa.Interval(), nullable=True))

    op.execute(f"UPDATE game SET use_cooldown = {sa.sql.expression.false()} WHERE use_cooldown IS NULL")

    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.alter_column('use_cooldown', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.drop_column('cooldown')
        batch_op.drop_column('use_cooldown')

from typing import List

from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pokras.game.tables.base import Base


class Game(Base):
    __tablename__ = "game"

    # id: int [pk, increment]
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # channel: int [not null]
    channel: Mapped[int] = mapped_column(nullable=False)

    # is_active: bool [default: false]
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    # Define the relationships to other tables.
    # The `back_populates` links the relationship on both sides.
    players: Mapped[List["Player"]] = relationship(
        back_populates="game",
        cascade="all, delete-orphan",  # Deletes players if the game is deleted
    )
    tiles: Mapped[List["Tile"]] = relationship(
        back_populates="game",
        cascade="all, delete-orphan",  # Deletes tiles if the game is deleted
    )

    def __repr__(self):
        return f"Game(id={self.id}, channel={self.channel}, is_active={self.is_active})"

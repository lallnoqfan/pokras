from typing import List

from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Enum

from db.base import Base
from game.tables.choices.game_map import GameMap


class Game(Base):
    __tablename__ = "game"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    channel: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    map: Mapped[GameMap] = mapped_column(Enum(GameMap, native_enum=False), nullable=False)

    countries: Mapped[List["Country"]] = relationship(
        back_populates="game",
        cascade="all, delete-orphan",
    )
    tiles: Mapped[List["Tile"]] = relationship(
        back_populates="game",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"Game(id={self.id}, channel={self.channel}, is_active={self.is_active}, map={self.map})"

from datetime import timedelta
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, Interval
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Enum

from db.base import Base
from modules.game.models.choices.game_map import GameMap

if TYPE_CHECKING:
    from modules.country.models.country import Country
    from modules.roll.models.tile import Tile
    from modules.roll.models.last_roll import LastRoll


class Game(Base):
    __tablename__ = "game"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    channel: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    map: Mapped[GameMap] = mapped_column(Enum(GameMap, native_enum=False), nullable=False)
    roll_values: Mapped[str] = mapped_column(String(100), nullable=False,
                                             default="1,1,1,1,1,1,1,1,1|3,5,9,15|4,7,7|2,3,5")
    use_cooldown: Mapped[bool] = mapped_column(Boolean, nullable=False)
    cooldown: Mapped[timedelta] = mapped_column(Interval, nullable=True)

    countries: Mapped[list["Country"]] = relationship(
        back_populates="game",
        cascade="all, delete-orphan",
    )
    tiles: Mapped[list["Tile"]] = relationship(
        back_populates="game",
        cascade="all, delete-orphan",
    )
    last_rolls: Mapped[list["LastRoll"]] = relationship(
        back_populates="game",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"Game(id={self.id}, channel={self.channel}, is_active={self.is_active}, map={self.map})"

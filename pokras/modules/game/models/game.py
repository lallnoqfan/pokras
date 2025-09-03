from datetime import timedelta
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, Interval
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Enum

from db.base import Base
from modules.game.models.choices.game_map import GameMap
from modules.roll.service.base.models.gamestate_things import GameState

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
    # tiles_num: Mapped[int] = mapped_column(nullable=False)
    # todo: общее количество тайлов на карте лучше брать из тайлера, чтобы не забивать бд
    neutral_tiles_num: Mapped[int] = mapped_column(nullable=False)

    roll_values: Mapped[str] = mapped_column(String(100), nullable=False)
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

    def cast(self) -> GameState:
        return GameState(
            id=self.id,
            channel=self.channel,
            is_active=self.is_active,
            map=self.map,
            roll_values=self.roll_values,
            use_cooldown=self.use_cooldown,
            cooldown=self.cooldown,
        )

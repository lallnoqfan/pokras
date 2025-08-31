from typing import Optional, TYPE_CHECKING

from sqlalchemy import UniqueConstraint, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from modules.roll.service.base.models.gamestate_things import TileState

if TYPE_CHECKING:
    from modules.game.models.game import Game
    from modules.country.models.country import Country


class Tile(Base):
    __tablename__ = "tile"
    __table_args__ = (
        UniqueConstraint("game_id", "code"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(5), nullable=False)

    game_id: Mapped[int] = mapped_column(ForeignKey("game.id", ondelete="CASCADE"), nullable=False)
    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("country.id", ondelete="CASCADE"), nullable=True)

    game: Mapped["Game"] = relationship(back_populates="tiles")
    owner: Mapped[Optional["Country"]] = relationship(back_populates="tiles")

    def __repr__(self):
        return f"Tile(id={self.id}, code='{self.code}', game_id={self.game_id}, owner_id={self.owner_id})"

    def cast(self) -> TileState:
        return TileState(
            id=self.id,
            code=self.code,
            game_id=self.game_id,
            owner_id=self.owner_id,
        )

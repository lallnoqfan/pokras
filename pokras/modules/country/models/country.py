from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from modules.game.models.game import Game
    from modules.roll.models.tile import Tile


class Country(Base):
    __tablename__ = "country"
    __table_args__ = (
        UniqueConstraint("game_id", "name"),
        UniqueConstraint("game_id", "color"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    color: Mapped[str] = mapped_column(String(7), nullable=False)
    creator_id: Mapped[int] = mapped_column(nullable=False)

    game_id: Mapped[int] = mapped_column(ForeignKey("game.id", ondelete="CASCADE"), nullable=False)

    game: Mapped["Game"] = relationship(back_populates="countries")
    tiles: Mapped[list["Tile"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"Country(id={self.id}, game_id={self.game_id}, name='{self.name}', color='{self.color}')"

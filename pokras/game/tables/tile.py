from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Tile(Base):
    __tablename__ = "tile"

    # id: int [pk, increment]
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # code: char [not null, unique]
    # We use String(1) for a single character.
    code: Mapped[str] = mapped_column(String(3), nullable=False, unique=True)

    # game: int [ref: > game.game.id, not null]
    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"), nullable=False)

    # owner: int [ref: > game.country.id] (optional/nullable)
    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("country.id"), nullable=True)

    game: Mapped["Game"] = relationship(back_populates="tiles")
    owner: Mapped[Optional["Country"]] = relationship(back_populates="tiles")

    def __repr__(self):
        return f"Tile(id={self.id}, code='{self.code}', game_id={self.game_id}, owner_id={self.owner_id})"

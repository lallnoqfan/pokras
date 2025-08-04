from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Player(Base):
    __tablename__ = "player"

    # id: int [pk, increment]
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # name: str [not null, unique]
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    # color: str [not null, unique]
    color: Mapped[str] = mapped_column(String(7), nullable=False, unique=True)

    # game_id: int [ref: > game.game.id, not null]
    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"), nullable=False)

    game: Mapped["Game"] = relationship(back_populates="players")

    tiles: Mapped[List["Tile"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"Player(id={self.id}, game_id={self.game_id}, name='{self.name}', color='{self.color}')"

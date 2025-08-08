from typing import Optional

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Tile(Base):
    __tablename__ = "tile"
    __table_args__ = (
        UniqueConstraint("game_id", "code"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(3), nullable=False)

    game_id: Mapped[int] = mapped_column(ForeignKey("game.id", ondelete="CASCADE"), nullable=False)
    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("country.id", ondelete="CASCADE"), nullable=True)

    game: Mapped["Game"] = relationship(back_populates="tiles")
    owner: Mapped[Optional["Country"]] = relationship(back_populates="tiles")

    def __repr__(self):
        return f"Tile(id={self.id}, code='{self.code}', game_id={self.game_id}, owner_id={self.owner_id})"

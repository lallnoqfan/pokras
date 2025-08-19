from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.base import Base
from db.datetime_utc import DatetimeUTC

if TYPE_CHECKING:
    from modules.game.models.game import Game
    from dataclasses import dataclass as dataclass_sql
else:
    def dataclass_sql(cls):
        return cls


@dataclass_sql
class LastRoll(Base):
    __tablename__ = "last_roll"
    __table_args__ = (
        UniqueConstraint("game_id", "user_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    game_id: Mapped[int] = mapped_column(ForeignKey("game.id", ondelete="CASCADE"), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DatetimeUTC, nullable=False)

    game: Mapped["Game"] = relationship(back_populates="last_rolls")

    def __repr__(self):
        return f"LastRoll(id={self.id}, user_id={self.user_id}, game_id={self.game_id}, timestamp={self.timestamp})"

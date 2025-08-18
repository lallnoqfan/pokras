from sqlalchemy import select

from db.engine import session
from modules.game.models.game import Game


def get_game_by_id(game_id: int) -> Game | None:
    stmt = select(Game).where(Game.id == game_id)
    return session.scalars(stmt).first()


def get_games_by_channel_id(channel_id: int) -> list[Game]:
    stmt = select(Game).where(Game.channel == channel_id)
    return session.scalars(stmt).all()


def get_active_game_by_channel_id(channel_id: int) -> Game | None:
    stmt = select(Game).where(Game.channel == channel_id, Game.is_active == True)
    return session.scalars(stmt).first()

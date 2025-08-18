from sqlalchemy import update

from db.engine import session
from modules.game.models.game import Game


def set_game_active(game_id: int) -> None:
    stmt = update(Game).where(Game.id == game_id).values(is_active=True)
    session.execute(stmt)
    session.commit()


def set_game_inactive(game_id: int) -> None:
    stmt = update(Game).where(Game.id == game_id).values(is_active=False)
    session.execute(stmt)
    session.commit()

from datetime import timedelta

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


def update_roll_values(game_id: int, values: str) -> None:
    stmt = update(Game).where(Game.id == game_id).values(roll_values=values)
    session.execute(stmt)
    session.commit()


def remove_cooldown(game_id: int) -> None:
    stmt = update(Game).where(Game.id == game_id).values(use_cooldown=False)
    session.execute(stmt)
    session.commit()


def set_cooldown(game_id: int, seconds: timedelta) -> None:
    stmt = update(Game).where(Game.id == game_id).values(use_cooldown=True, cooldown=seconds)
    session.execute(stmt)
    session.commit()

from sqlalchemy import select

from db.engine import session
from modules.roll.models.last_roll import LastRoll


def get_last_roll(game_id: int, user_id: int) -> LastRoll | None:
    stmt = select(LastRoll).where(LastRoll.game_id == game_id, LastRoll.user_id == user_id)
    return session.scalars(stmt).first()

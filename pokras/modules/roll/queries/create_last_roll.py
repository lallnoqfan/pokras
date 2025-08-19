from datetime import datetime

from db.engine import session
from modules.roll.models.last_roll import LastRoll


def create_last_roll(game_id: int, user_id: int, timestamp: datetime) -> LastRoll:
    new_last_roll = LastRoll(game_id=game_id, user_id=user_id, timestamp=timestamp)
    session.add(new_last_roll)
    session.commit()
    session.refresh(new_last_roll)
    return new_last_roll

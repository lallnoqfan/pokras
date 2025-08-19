from datetime import datetime

from sqlalchemy import update

from db.engine import session
from modules.roll.models.last_roll import LastRoll


def set_last_roll_timestamp(last_roll_id: int, timestamp: datetime) -> None:
    stmt = update(LastRoll).where(LastRoll.id == last_roll_id).values(timestamp=timestamp)
    session.execute(stmt)
    session.commit()

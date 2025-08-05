from sqlalchemy import select

from db.engine import session
from game.tables import Tile


def get_tile(code: str, game_id: int) -> Tile | None:
    stmt = select(Tile).where(Tile.code == code, Tile.game_id == game_id)
    return session.scalars(stmt).first()

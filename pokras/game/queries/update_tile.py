from sqlalchemy import update

from db.engine import session
from game.tables import Tile


def update_tile_owner(game_id: int, tile_code: str, new_owner_id: int) -> None:
    stmt = (update(Tile)
            .where(Tile.game_id == game_id, Tile.code == tile_code)
            .values(owner_id=new_owner_id))
    session.execute(stmt)

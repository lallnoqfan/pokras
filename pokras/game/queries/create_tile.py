from db.engine import session
from game.tables import Tile


def create_tile(code: str, game_id: int, owner_id: int) -> Tile:
    new_tile = Tile(code=code, game_id=game_id, owner_id=owner_id)
    session.add(new_tile)
    session.commit()
    session.refresh(new_tile)
    return new_tile

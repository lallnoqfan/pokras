from game.games.base.repository.repository import Repository
from game.queries.create_tile import create_tile
from game.queries.get_tile import get_tile
from game.queries.update_tile import update_tile_owner
from game.tables import Game, Country


class BaseRepository(Repository):
    """
    Базовая реализация репозитория.
    """
    @classmethod
    def get_tile_owner(cls, game: Game, tile_code: str) -> Country | None:
        tile = get_tile(tile_code, game.id)
        if not tile:
            return None
        return tile.owner

    @classmethod
    def set_tile_owner(cls, game: Game, country: Country, tile_code: str) -> None:
        tile = get_tile(tile_code, game.id)
        if not tile:
            create_tile(tile_code, game.id, country.id)
        else:
            update_tile_owner(game.id, tile_code, country.id)

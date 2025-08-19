from datetime import datetime

from modules.country.models.country import Country
from modules.game.models.game import Game
from modules.game.service.models.roll_values import RollValues
from modules.game.service.service import get_roll_values
from modules.roll.models.last_roll import LastRoll
from modules.roll.queries.create_tile import create_tile
from modules.roll.queries.get_last_roll import get_last_roll
from modules.roll.queries.get_tile import get_tile
from modules.roll.queries.update_last_roll import set_last_roll_timestamp
from modules.roll.queries.update_tile import update_tile_owner
from modules.roll.service.base.repository.repository import Repository


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

    @classmethod
    def get_roll_values(cls, game: Game) -> RollValues:
        return get_roll_values(game)

    @classmethod
    def get_last_roll(cls, game: Game, country: Country) -> LastRoll | None:
        return get_last_roll(game.id, country.id)

    @classmethod
    def set_last_roll(cls, game: Game, country: Country, timestamp: datetime) -> None:
        last_roll = get_last_roll(game.id, country.id)
        if last_roll is None:
            return
        set_last_roll_timestamp(last_roll.id, timestamp)

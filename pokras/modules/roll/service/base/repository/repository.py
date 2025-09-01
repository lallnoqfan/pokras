from datetime import datetime

from modules.country.queries.get_country import get_country_by_name, get_country
from modules.game.queries.get_game import get_game_by_id
from modules.game.service.models.roll_values import RollValues
from modules.game.service.service import get_roll_values
from modules.roll.models.last_roll import LastRoll
from modules.roll.queries.create_last_roll import create_last_roll
from modules.roll.queries.create_tile import create_tile
from modules.roll.queries.get_last_roll import get_last_roll
from modules.roll.queries.get_tile import get_tile
from modules.roll.queries.update_last_roll import update_last_roll_timestamp
from modules.roll.queries.update_tile import update_tile_owner
from modules.roll.service.base.models.gamestate_things import GameState, CountryState, TileState


class Repository:
    """
    Класс, отвечающий за чтение состояния игры.
    Прячет внутри себя доступ к бд / другому хранилищу состояния.
    """
    @classmethod
    def get_country_by_name(cls, game: GameState, country_name: str) -> CountryState | None:
        country = get_country_by_name(game.id, country_name)
        if not country:
            return None
        return country.cast()

    @classmethod
    def get_tile_owner(cls, game: GameState, tile_code: str) -> CountryState | None:
        tile = get_tile(tile_code, game.id)
        if not tile:
            return None
        return tile.owner.cast()

    @classmethod
    def set_tile_owner(cls, game: GameState, country: CountryState, tile_code: str) -> None:
        tile = get_tile(tile_code, game.id)
        if not tile:
            create_tile(tile_code, game.id, country.id)
        else:
            update_tile_owner(game.id, tile_code, country.id)

    @classmethod
    def get_roll_values(cls, game: GameState) -> RollValues:
        game = get_game_by_id(game.id)
        return get_roll_values(game)

    @classmethod
    def get_last_roll(cls, game: GameState, country: CountryState) -> LastRoll | None:
        # todo replace with dataclass model
        return get_last_roll(game.id, country.id)

    @classmethod
    def set_last_roll(cls, game: GameState, country: CountryState, timestamp: datetime) -> None:
        last_roll = get_last_roll(game.id, country.id)
        if last_roll is None:
            create_last_roll(game.id, country.id, timestamp)
        else:
            update_last_roll_timestamp(last_roll.id, timestamp)

    @classmethod
    def get_country_tiles(cls, country: CountryState) -> list[TileState]:
        country = get_country(country.id)
        if country is None:
            return []
        return list(map(lambda tile: tile.cast(), country.tiles))

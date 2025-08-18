from abc import ABC

from modules.country.models.country import Country
from modules.game.models.game import Game
from modules.roll.responses import RollResponses
from modules.roll.service.base.service.base_service import BaseService
from modules.roll.service.base.tiler.spawn_prohibited_tiler import SpawnProhibitedTiler


class SpawnProhibitedService(BaseService, ABC):
    @classmethod
    def _spawn(cls, game: Game, country: Country, roll_value: int, tile_codes: list[str], response: list[str]) -> int:
        if not issubclass(cls.tiler, SpawnProhibitedTiler):
            raise ValueError(f"service's tiler must be SpawnRestrictedTiler, got {cls.tiler.__class__.__name__}")

        spawn_tile = None
        for tile_code in tile_codes:
            if cls.tiler.can_spawn(tile_code):
                spawn_tile = tile_code
                break

        if spawn_tile is None:
            response.append(RollResponses.spawn_restricted_tiles())
            return roll_value
        tile_codes.remove(spawn_tile)

        # some dirty code repetition here
        # if some other spawn related mechanic will be added, this should be refactored

        tile_owner: Country = cls.repository.get_tile_owner(game, spawn_tile)

        if tile_owner is None:
            response.append(RollResponses.spawn(country.name, spawn_tile))
        else:
            response.append(RollResponses.spawn_attack(country.name, spawn_tile, tile_owner.name))

        cls.repository.set_tile_owner(game, country, spawn_tile)
        roll_value -= 1

        return roll_value

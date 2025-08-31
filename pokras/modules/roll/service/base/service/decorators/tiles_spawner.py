from modules.roll.responses import RollResponses
from modules.roll.service.base.models.api_things import TilesRollPrompt, RollResponse
from modules.roll.service.base.models.gamestate_things import GameState, CountryState
from modules.roll.service.base.service.abc.service_decorator import ServiceDecorator


class TilesSpawner(ServiceDecorator):
    def __spawn(self, game: GameState, country: CountryState,
                spawn_tile: str, roll_value: int, response: list[str]) -> int:
        previous_owner = self.repository.get_tile_owner(game, spawn_tile)

        self.repository.set_tile_owner(game, country, spawn_tile)
        roll_value -= 1

        if previous_owner is None:
            response.append(RollResponses.spawn(country.name, spawn_tile))
        else:
            response.append(RollResponses.spawn_attack(country.name, spawn_tile, previous_owner.name))

        return roll_value

    def _pick_spawn_tile(self, game: GameState, country: CountryState,
                         tile_codes: list[str], response: list[str]) -> str | None:
        return tile_codes.pop(0)

    def add_tiles(self, game: GameState, prompt: TilesRollPrompt) -> RollResponse:
        country = self.repository.get_country_by_name(game, prompt.country)
        country_tiles = self.repository.get_country_tiles(country)
        if country_tiles:  # todo replace with tiles counter
            return self._service.add_tiles(game, prompt)

        response = []

        roll_value = prompt.roll_value
        spawn_tile = self._pick_spawn_tile(game, country, prompt.tiles, response)
        if spawn_tile is None:
            response.append(RollResponses.roll_value_surplus(roll_value))
            return RollResponse(ok=False, map_state_changed=False, messages=response)

        new_roll_value = self.__spawn(game, country, spawn_tile, roll_value, response)
        spawn_succeed = new_roll_value < roll_value
        if not spawn_succeed:
            response.append(RollResponses.roll_value_surplus(roll_value))
            return RollResponse(ok=False, map_state_changed=False, messages=response)
        prompt.roll_value = new_roll_value

        service_response = self._service.add_tiles(game, prompt)
        response.extend(service_response.messages)
        return RollResponse(ok=True, map_state_changed=True, messages=response)


class TilesRestrictedSpawner(TilesSpawner):
    def _pick_spawn_tile(self, game: GameState, country: CountryState,
                         tile_codes: list[str], response: list[str]) -> str | None:
        for tile_code in tile_codes:
            if self.tiler.can_spawn(tile_code):
                tile_codes.remove(tile_code)
                return tile_code

        response.append(RollResponses.spawn_restricted_tiles())
        return None

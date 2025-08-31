from modules.country.responses import CountryResponses
from modules.roll.responses import RollResponses
from modules.roll.service.base.models.api_things import RollResponse, AgainstRollPrompt, ExpansionRollPrompt, \
    TilesRollPrompt
from modules.roll.service.base.models.gamestate_things import GameState, CountryState
from modules.roll.service.base.service.abc.validator import Validator


class TilesValidator(Validator):
    def __filter_non_existing_tiles(self, tile_codes: list[str], response: list[str]) -> list[str]:
        valid_tiles = []
        invalid_tiles = []
        for tile_code in tile_codes:
            if not self.tiler.tile_exists(tile_code):
                invalid_tiles.append(tile_code)
            else:
                valid_tiles.append(tile_code)
        if invalid_tiles:
            if len(invalid_tiles) == 1:
                response.append(RollResponses.invalid_tile(invalid_tiles[0]))
            else:
                response.append(RollResponses.invalid_tiles(invalid_tiles))
        return valid_tiles

    def __filter_own_tiles(self, game: GameState, country: CountryState,
                           tile_codes: list[str], response: list[str]) -> list[str]:
        valid_tiles = []
        invalid_tiles = []
        for tile_code in tile_codes:
            tile_owner = self.repository.get_tile_owner(game, tile_code)
            if tile_owner is not None and tile_owner.id == country.id:
                invalid_tiles.append(tile_code)
            else:
                valid_tiles.append(tile_code)
        if invalid_tiles:
            response.append(RollResponses.capture_own_tiles(invalid_tiles))
        return valid_tiles

    def validate_tiles(self, game: GameState, prompt: TilesRollPrompt) -> RollResponse | None:
        response = []

        country = self.repository.get_country_by_name(game, prompt.country)
        if country is None:
            response.append(CountryResponses.country_not_found(prompt.country))
            return RollResponse(ok=False, map_state_changed=False, messages=response)

        tile_codes = self.parser.parse_tiles(self.tiler, prompt.tiles)
        tile_codes = self.__filter_non_existing_tiles(tile_codes, response)
        tile_codes = self.__filter_own_tiles(game, country, tile_codes, response)
        if not tile_codes:
            response.append("No valid tiles were provided")  # todo: move to responses
            return RollResponse(ok=False, map_state_changed=False, messages=response)
        prompt.tiles = tile_codes

        return None

    def validate_expansion(self, game: GameState, prompt: ExpansionRollPrompt) -> RollResponse | None:
        response = []

        country = self.repository.get_country_by_name(game, prompt.country)
        if country is None:
            response.append(CountryResponses.country_not_found(prompt.country))
            return RollResponse(ok=False, map_state_changed=False, messages=response)

        country_tiles = self.repository.get_country_tiles(country)  # todo add tiles counter to state
        if not country_tiles:
            response.append(RollResponses.expansion_without_tiles())
            return RollResponse(ok=False, map_state_changed=False, messages=response)

        return None

    def validate_against(self, game: GameState, prompt: AgainstRollPrompt) -> RollResponse | None:
        response = []

        if prompt.country == prompt.target:
            response.append(RollResponses.against_self())
            return RollResponse(ok=False, map_state_changed=False, messages=response)

        country = self.repository.get_country_by_name(game, prompt.country)
        if country is None:
            response.append(CountryResponses.country_not_found(prompt.country))
            return RollResponse(ok=False, map_state_changed=False, messages=response)

        target = self.repository.get_country_by_name(game, prompt.target)
        if target is None:
            response.append(CountryResponses.country_not_found(prompt.target))
            return RollResponse(ok=False, map_state_changed=False, messages=response)

        country_tiles = self.repository.get_country_tiles(country)  # todo add tiles counter to state
        if not country_tiles:
            response.append(RollResponses.against_without_tiles())
            return RollResponse(ok=False, map_state_changed=False, messages=response)

        target_tiles = self.repository.get_country_tiles(target)  # todo add tiles counter to state
        if not target_tiles:
            response.append(RollResponses.against_target_has_no_tiles(target.name))
            return RollResponse(ok=False, map_state_changed=False, messages=response)

        return None

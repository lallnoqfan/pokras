from collections import defaultdict

from modules.roll.responses import RollResponses
from modules.roll.service.base.models.api_things import TilesRollPrompt, ExpansionRollPrompt, AgainstRollPrompt, \
    RollResponse
from modules.roll.service.base.models.gamestate_things import GameState
from modules.roll.service.base.service.abc.service import Service


class LiveTilesService(Service):
    """
    Real time сервис для карт с именованными тайлами.
    """
    # all that stuff might be quite slow... should consider adding db locks
    def add_tiles(self, game: GameState, prompt: TilesRollPrompt) -> RollResponse:
        response = []
        state_changed = False

        country = self.repository.get_country_by_name(game, prompt.country)
        tile_codes = prompt.tiles
        roll_value = initial_roll_value = prompt.roll_value

        while roll_value > 0 and tile_codes:
            country_tiles = self.repository.get_country_tiles(country)
            # now the hard(?) part. since not all tiles might be reachable from input order,
            # but with capturing other tiles they might become reachable,
            # we need to check them all again and again while there is still some roll value
            #
            # i dont really like this loop
            were_captures = False
            owned_tiles = set(tile.code for tile in country_tiles)
            # yes we load ALL country's tiles...might be stupid dunno

            for tile_code in tile_codes:
                for adjacent_tile_code in self.tiler.get_adjacent_tiles(tile_code):
                    if adjacent_tile_code not in owned_tiles:
                        continue
                    were_captures = True
                    state_changed = True

                    tile_owner = self.repository.get_tile_owner(game, tile_code)
                    if tile_owner is None:
                        response.append(RollResponses.capture_neutral(country.name, tile_code))
                    else:
                        response.append(RollResponses.capture_attack(country.name, tile_owner.name, tile_code))

                    self.repository.set_tile_owner(game, country, tile_code)
                    tile_codes.remove(tile_code)
                    roll_value -= 1
                    break

                if were_captures:
                    break  # so we can return to tiles original order
            if were_captures:
                continue

            # no connected tiles remaining
            for tile_code in tile_codes:  # and there is still some roll value
                response.append(RollResponses.capture_no_route(tile_code))
            break

        if roll_value == initial_roll_value:
            ok = False
            # todo add roll failed message
        elif roll_value > 0:
            ok = True
            response.append(RollResponses.roll_value_surplus(roll_value))
        else:  # roll_value == 0
            ok = True

        return RollResponse(ok=ok, map_state_changed=state_changed, messages=response)

    def add_expansion(self, game: GameState, prompt: ExpansionRollPrompt) -> RollResponse:
        # this thing chooses somewhat nearest tiles to the country
        # the way it interprets the "nearest" though is kinda not the best one
        #
        # it calcs distances between country's tiles and adjacent to them tiles
        # and then picks the closest adjacent tile to one of the country's tiles
        #
        # it leads to not what you would call "nearest" tiles selection pattern
        # maybe some other way like picking the closest neutral tile to mass centroid of the country
        # would do the job better
        #
        # but for now i don't care
        response = []
        state_changed = False

        country = self.repository.get_country_by_name(game, prompt.country)
        roll_value = initial_roll_value = prompt.roll_value

        free_tiles_codes = defaultdict(lambda: float("inf"))
        visited = set()

        while roll_value > 0:
            # damn thats should be expensive server resources wise
            # ...
            # so ive checked this code, and actually, after we added one tile to the country
            # we would check ALL ITS TILES again for like nothing 'cause we only need to check ONE added tile...
            # yeah, i know that all visited tiles are already in the set, so it wouldn't take that long
            # but still some queue-ish structure would be really nice
            country_tiles = self.repository.get_country_tiles(country)
            for tile in country_tiles:
                tile_code = tile.code
                if tile_code in visited:
                    continue
                visited.add(tile_code)

                adjacent_tiles = self.tiler.get_adjacent_tiles(tile_code)
                for adjacent_tile_code in adjacent_tiles:
                    tile_owner = self.repository.get_tile_owner(game, adjacent_tile_code)
                    if tile_owner is not None:
                        continue

                    distance = self.tiler.calc_distance(tile_code, adjacent_tile_code)
                    free_tiles_codes[adjacent_tile_code] = min(free_tiles_codes[adjacent_tile_code], distance)

            if not free_tiles_codes:
                break

            nearest_tile_code = min(free_tiles_codes, key=free_tiles_codes.get)
            self.repository.set_tile_owner(game, country, nearest_tile_code)

            roll_value -= 1
            free_tiles_codes.pop(nearest_tile_code)
            response.append(RollResponses.capture_neutral(country.name, nearest_tile_code))
            state_changed = True

        if roll_value == initial_roll_value:
            ok = False
            # todo add roll failed message
            response.append(RollResponses.expansion_no_free_tiles())
        elif roll_value > 0:
            ok = True
            response.append(RollResponses.expansion_no_free_tiles())
            response.append(RollResponses.roll_value_surplus(roll_value))
        else:  # roll_value == 0
            ok = True

        return RollResponse(ok=ok, map_state_changed=state_changed, messages=response)

    def add_against(self, game: GameState, prompt: AgainstRollPrompt) -> RollResponse:
        # works pretty much in the same way as _add_tiles_expansion
        # the only difference is that it chooses not neutral tiles but targets tiles
        response = []
        state_changed = False

        country = self.repository.get_country_by_name(game, prompt.country)
        target = self.repository.get_country_by_name(game, prompt.target)
        roll_value = initial_roll_value = prompt.roll_value

        target_tiles = defaultdict(lambda: float("inf"))
        visited = set()

        while roll_value > 0:
            country_tiles = self.repository.get_country_tiles(country)
            for tile in country_tiles:
                tile_code = tile.code
                if tile_code in visited:
                    continue
                visited.add(tile_code)

                for adjacent_tile_code in self.tiler.get_adjacent_tiles(tile_code):
                    tile_owner = self.repository.get_tile_owner(game, adjacent_tile_code)
                    if (tile_owner is None) or (tile_owner.id != target.id):
                        continue

                    distance = self.tiler.calc_distance(tile_code, adjacent_tile_code)
                    target_tiles[adjacent_tile_code] = min(target_tiles[adjacent_tile_code], distance)

            if not target_tiles:
                break

            nearest = min(target_tiles, key=target_tiles.get)
            self.repository.set_tile_owner(game, country, nearest)

            roll_value -= 1
            target_tiles.pop(nearest)
            response.append(RollResponses.capture_attack(country.name, target.name, nearest))
            state_changed = True

        if roll_value == initial_roll_value:
            ok = False
            response.append(RollResponses.against_no_routes(target.name))
            # todo add roll failed message
        elif roll_value > 0:
            ok = True
            response.append(RollResponses.against_no_routes(target.name))
            response.append(RollResponses.roll_value_surplus(roll_value))
        else:  # roll_value == 0
            ok = True

        return RollResponse(ok=ok, map_state_changed=state_changed, messages=response)

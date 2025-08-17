from abc import ABC
from collections import defaultdict

from game.games.base.service.service import Service
from game.responses.roll import RollResponses
from game.tables import Game, Country


class BaseService(Service, ABC):
    """
    Базовая реализация сервиса.
    """
    # all that stuff might be quite slow... should consider adding db locks

    @classmethod
    def _validate_tiles_exist(cls, tile_codes: list[str], response: list[str]) -> list[str]:
        """
        Фильтрует тайлы, которых нет на карте.
        В случае наличия, добавляет сообщение в response.

        Args:
            tile_codes: список тайлов, на которые страна роллит
            response: ответ

        Returns:
            Список тайлов, которые есть на карте
        """
        valid_tiles = []
        invalid_tiles = []
        for tile_code in tile_codes:
            if cls.tiler.tile_exists(tile_code):
                valid_tiles.append(tile_code)
            else:
                invalid_tiles.append(tile_code)
        if invalid_tiles:
            response.append(RollResponses.invalid_tiles(invalid_tiles))
        return valid_tiles

    @classmethod
    def _validate_doesnt_own_tiles(cls, game: Game, country: Country,
                                   tile_codes: list[str], response: list[str]) -> list[str]:
        """
        Фильтрует тайлы, уже принадлежащие игроку.
        В случае наличия, добавляет сообщение в response.

        Args:
             game: моделька игры
             country: моделька страны, которая роллит
             tile_codes: список тайлов, на которые страна роллит
             response: ответ

        Returns:
            Список тайлов, не принадлежащих игроку
        """
        valid_tiles = []
        invalid_tiles = []
        for tile_code in tile_codes:
            tile_owner: Country = cls.repository.get_tile_owner(game, tile_code)
            if tile_owner is None or tile_owner.id != country.id:
                valid_tiles.append(tile_code)
            else:
                invalid_tiles.append(tile_code)
        if invalid_tiles:
            response.append(RollResponses.capture_own_tiles(invalid_tiles))
        return valid_tiles

    @classmethod
    def _spawn(cls, game: Game, country: Country, roll_value: int, tile_codes: list[str], response: list[str]) -> int:
        spawn_tile = tile_codes.pop(0)
        tile_owner: Country = cls.repository.get_tile_owner(game, spawn_tile)

        if tile_owner is None:
            response.append(RollResponses.spawn(country.name, spawn_tile))
        else:
            response.append(RollResponses.spawn_attack(country.name, spawn_tile, tile_owner.name))

        cls.repository.set_tile_owner(game, country, spawn_tile)
        roll_value -= 1

        return roll_value

    @classmethod
    def add_tiles(cls, game: Game, country: Country, roll_value: int, tiles: str | list[str]) -> tuple[int, list[str]]:
        response = []
        tile_codes = cls.parser.parse_tiles(cls.tiler, tiles)
        tile_codes = cls._validate_tiles_exist(tile_codes, response)
        tile_codes = cls._validate_doesnt_own_tiles(game, country, tile_codes, response)

        if roll_value <= 0:
            return roll_value, response

        if not country.tiles:
            new_roll_value = cls._spawn(game, country, roll_value, tile_codes, response)
            if new_roll_value == roll_value:  # that is, spawn failed, so we should break; it's kinda lame though
                return roll_value, response

        while roll_value > 0 and tile_codes:
            # now the hard(?) part. since not all tiles might be reachable from input order,
            # but with capturing other tiles they might become reachable,
            # we need to check them all again and again while there is still some roll value
            #
            # i dont really like this loop
            were_captures = False
            owned_tiles = set(tile.code for tile in country.tiles)  # noqa: shut up
            # yes we load ALL country's tiles...might be stupid dunno

            for tile_code in tile_codes:
                for adjacent_tile_code in cls.tiler.get_adjacent_tiles(tile_code):
                    if adjacent_tile_code not in owned_tiles:
                        continue
                    were_captures = True

                    tile_owner: Country = cls.repository.get_tile_owner(game, tile_code)

                    if tile_owner is None:
                        response.append(RollResponses.capture_neutral(country.name, tile_code))
                    else:
                        response.append(RollResponses.capture_attack(country.name, tile_owner.name, tile_code))

                    cls.repository.set_tile_owner(game, country, tile_code)

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

        if roll_value > 0:
            response.append(RollResponses.roll_value_surplus(roll_value))

        return roll_value, response

    @classmethod
    def add_expansion(cls, game: Game, country: Country, roll_value: int) -> tuple[int, list[str]]:
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

        if not country.tiles:
            response.append(RollResponses.expansion_without_tiles())
            return roll_value, response

        if roll_value <= 0:
            return roll_value, response

        free_tiles_codes = defaultdict(lambda: float("inf"))
        visited = set()

        while roll_value > 0:
            # damn thats should be expensive server resources wise
            # ...
            # so ive checked this code, and actually, after we added one tile to the country
            # we would check ALL ITS TILES again for like nothing 'cause we only need to check ONE added tile...
            # yeah, i know that all visited tiles are already in the set, so it wouldn't take that long
            # but still some queue-ish structure would be really nice
            for tile in country.tiles:
                tile_code = tile.code
                if tile_code in visited:
                    continue
                visited.add(tile_code)

                adjacent_tiles = cls.tiler.get_adjacent_tiles(tile_code)
                for adjacent_tile_code in adjacent_tiles:
                    tile_owner = cls.repository.get_tile_owner(game, adjacent_tile_code)
                    if tile_owner:
                        continue

                    distance = cls.tiler.calc_distance(tile_code, adjacent_tile_code)
                    free_tiles_codes[adjacent_tile_code] = min(free_tiles_codes[adjacent_tile_code], distance)

            if not free_tiles_codes:
                break

            nearest_tile_code = min(free_tiles_codes, key=free_tiles_codes.get)
            cls.repository.set_tile_owner(game, country, nearest_tile_code)

            roll_value -= 1
            free_tiles_codes.pop(nearest_tile_code)
            response.append(RollResponses.capture_neutral(country.name, nearest_tile_code))

        if roll_value > 0:
            response.append(RollResponses.expansion_no_free_tiles())

        return roll_value, response

    @classmethod
    def add_against(cls, game: Game, country: Country, target: Country, roll_value: int) -> tuple[int, list[str]]:
        # works pretty much in the same way as _add_tiles_expansion
        # the only difference is that it chooses not neutral tiles but targets tiles
        response = []

        if not country.tiles:
            response.append(RollResponses.against_without_tiles())
            return roll_value, response

        if not target.tiles:
            response.append(RollResponses.against_target_has_no_tiles(target.name))
            return roll_value, response

        if country.name == target.name:
            response.append(RollResponses.against_self())
            return roll_value, response

        if roll_value <= 0:
            return roll_value, response

        target_tiles = defaultdict(lambda: float("inf"))
        visited = set()

        while roll_value > 0:
            for tile in country.tiles:
                tile_code = tile.code
                if tile_code in visited:
                    continue
                visited.add(tile_code)

                for adjacent_tile_code in cls.tiler.get_adjacent_tiles(tile_code):
                    tile_owner = cls.repository.get_tile_owner(game, adjacent_tile_code)
                    if tile_owner is None or tile_owner.id != target.id:
                        continue

                    distance = cls.tiler.calc_distance(tile_code, adjacent_tile_code)
                    target_tiles[adjacent_tile_code] = min(target_tiles[adjacent_tile_code], distance)

            if not target_tiles:
                break

            nearest = min(target_tiles, key=target_tiles.get)
            cls.repository.set_tile_owner(game, country, nearest)
            roll_value -= 1
            target_tiles.pop(nearest)
            response.append(RollResponses.capture_attack(country.name, target.name, nearest))

        if roll_value > 0:
            response.append(RollResponses.against_no_routes(target.name))

        return roll_value, response

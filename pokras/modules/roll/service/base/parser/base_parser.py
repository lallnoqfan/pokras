from re import match, findall
from typing import Type

from modules.roll.service.base.parser.parser import Parser
from modules.roll.service.base.tiler.tiler import Tiler
from utils.text import cyrillic_to_roman


class BaseParser(Parser):
    @classmethod
    def parse_tiles(cls, _: Type[Tiler], tiles: str | list[str]) -> list[str]:
        if isinstance(tiles, list):
            result = []
            for t in tiles:
                result.extend(cls.parse_tiles(_, t))
            return result

        tiles = tiles.lower()  # "2B 3Ф" -> "2b 3ф"
        tiles = cyrillic_to_roman(tiles)  # "2b 3ф" -> "2b 3f"
        tiles = tiles.split()  # "2b 3f" -> ["2b", "3f"]

        # ["1a2b3cd"] -> ["1a", "2b", "3cd"]
        i = 0
        while i < len(tiles):
            res = findall(r"\d+[a-z]+", tiles[i])

            if len(res) <= 1:
                i += 1
                continue

            tiles.pop(i)
            for s in res:
                tiles.insert(i, s)
                i += 1

        # ["1abc"] -> ["1a", "1b", "1c"]
        i = 0
        while i < len(tiles):
            res = match(r"(\d+)([a-zA-Z]{2,})", tiles[i])

            if not res:
                i += 1
                continue

            tiles.pop(i)
            for s in [res.group(1) + c for c in res.group(2)]:
                tiles.insert(i, s)
                i += 1

        # duplicates clearing
        tiles = list(set(tiles))
        tiles.sort()
        # todo: it would be great if we could preserve initial order of tiles tiles as it is in user's input
        #       for now, after parsing, initial order is totally lost, so should probably be fixed

        return tiles

    @classmethod
    def get_roll_value(cls, roll: str | int | list[int]) -> int:
        if isinstance(roll, int):
            roll = str(roll)
        elif isinstance(roll, list):
            roll = "".join(str(r) for r in roll)

        patterns = {}

        result_roll_value = 1

        for pattern in patterns.keys():
            if match(pattern, roll):
                result_roll_value = max(result_roll_value, patterns[pattern])

        return result_roll_value

from typing import Type

from modules.roll.service.base.parser.base_parser import BaseParser
from modules.roll.service.base.tiler.aliases_tiler import AliasesTiler
from modules.roll.service.base.tiler.tiler import Tiler


class AliasesParser(BaseParser):
    @classmethod
    def parse_tiles(cls, tiler: Type[Tiler], tiles: str) -> list[str]:
        if not issubclass(tiler, AliasesTiler):
            raise ValueError(f"tiler must be AliasesTiler, got {tiler.__class__.__name__}")

        if isinstance(tiles, list):
            result = []
            for t in tiles:
                result.extend(cls.parse_tiles(tiler, t))
            return result

        tiles = tiles.lower()
        tiles = tiles.split()
        tiles = [tiler.get_alias(t) for t in tiles]
        tiles = " ".join(tiles)
        return super().parse_tiles(tiler, tiles)

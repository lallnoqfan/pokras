from modules.roll.service.base.parser.base_parser import BaseParser
from modules.roll.service.base.tiler.decorators.aliases_tiler import AliasesTiler


class AliasesParser(BaseParser):
    def parse_tiles(self, tiler: AliasesTiler, tiles: list[str]) -> list[str]:
        tiles = " ".join(tiles)

        tiles = tiles.lower()
        tiles = tiles.split()
        tiles = list(map(tiler.get_by_alias, tiles))
        return super().parse_tiles(tiler, tiles)

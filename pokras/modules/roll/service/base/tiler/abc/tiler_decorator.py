from abc import ABC

from modules.roll.service.base.models.mapdata_things import MapData, TileSchema
from modules.roll.service.base.tiler.abc.tiler import Tiler


class TilerDecorator(Tiler, ABC):
    def __init__(self, tiler: Tiler):
        super().__init__(tiler.data_path)
        self._tiler = tiler

    def _load_data(self) -> MapData:
        return self._tiler._load_data()

    def _get_tiles(self) -> dict[str, TileSchema]:
        return self._tiler._get_tiles()

    def _get_tile(self, tile_code: str) -> TileSchema | None:
        return self._tiler._get_tile(tile_code)

    def get_by_alias(self, alias: str) -> str:
        return self._tiler.get_by_alias(alias)

    def get_fill_cords(self, tile_code: str) -> tuple[int, int]:
        return self._tiler.get_fill_cords(tile_code)

    def get_center_cords(self, tile_code: str) -> tuple[int, int]:
        return self._tiler.get_center_cords(tile_code)

    def get_adjacent_tiles(self, tile_code: str) -> frozenset[str]:
        return self._tiler.get_adjacent_tiles(tile_code)

    def get_tile_bonus(self, tile_code: str) -> int:
        return self._tiler.get_tile_bonus(tile_code)

    def tile_exists(self, tile_code: str) -> bool:
        return self._tiler.tile_exists(tile_code)

    def can_spawn(self, tile_code: str) -> bool:
        return self._tiler.can_spawn(tile_code)

    def calc_distance(self, first_tile_code: str, second_tile_code: str) -> float:
        return self._tiler.calc_distance(first_tile_code, second_tile_code)

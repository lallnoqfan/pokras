from abc import ABC
from functools import cache
from json import load

from modules.roll.service.base.models.mapdata_things import MapData, TileSchema
from modules.roll.service.base.tiler.abc.tiler import Tiler


class BaseTiler(Tiler, ABC):
    """
    Базовая реализация тайлера
    """
    @cache
    def _load_data(self) -> MapData:
        with self.data_path.open("r", encoding="utf-8") as data_file:
            return MapData(**load(data_file))

    def _get_tiles(self) -> dict[str, TileSchema]:
        return self._load_data().tiles

    def _get_tile(self, tile_code: str) -> TileSchema | None:
        return self._get_tiles().get(tile_code, None)

    def get_by_alias(self, alias: str) -> str:
        return alias

    def get_fill_cords(self, tile_code: str) -> tuple[int, int]:
        return self._get_tile(tile_code).fill_cords

    def get_center_cords(self, tile_code: str) -> tuple[int, int]:
        return self._get_tile(tile_code).center_cords

    def get_adjacent_tiles(self, tile_code: str) -> frozenset[str]:
        return self._get_tile(tile_code).routes

    def get_tile_bonus(self, tile_code: str) -> int:
        return 0

    def tile_exists(self, tile_code: str) -> bool:
        return tile_code in self._get_tiles()

    def can_spawn(self, tile_code: str) -> bool:
        return True

    def calc_distance(self, first_tile_code: str, second_tile_code: str) -> float:
        x1, y1 = self.get_fill_cords(first_tile_code)
        x2, y2 = self.get_fill_cords(second_tile_code)
        distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        return distance

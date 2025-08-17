from abc import ABC
from functools import cache
from json import load

from game.games.base.tiler.tiler import Tiler


class BaseTiler(Tiler, ABC):
    """
    Базовая реализация тайлера
    """
    @classmethod
    @cache
    def _load_data(cls) -> dict:
        with cls.DATA_PATH.open("r", encoding="utf-8") as tiles_data:
            return load(tiles_data)

    @classmethod
    def _get_tiles(cls) -> dict:
        return cls._load_data().get("tiles")

    @classmethod
    def _get_tile(cls, tile_code: str) -> dict | None:
        return cls._get_tiles().get(tile_code, None)

    @classmethod
    def tile_exists(cls, tile_code: str) -> bool:
        return tile_code in cls._get_tiles()

    @classmethod
    def get_fill_cords(cls, tile_code: str) -> tuple[int, int]:
        tile = cls._get_tile(tile_code)
        x, y = tile.get("fill_cords")
        return x, y

    @classmethod
    def get_adjacent_tiles(cls, tile_code: str) -> list[str]:
        tile = cls._get_tile(tile_code)
        return tile.get("routes")

    @classmethod
    def calc_distance(cls, first_tile_code: str, second_tile_code: str) -> float:
        x1, y1 = cls.get_fill_cords(first_tile_code)
        x2, y2 = cls.get_fill_cords(second_tile_code)
        distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        return distance

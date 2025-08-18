from abc import ABC

from modules.roll.service.base.tiler.base_tiler import BaseTiler


class LegacyTiler(BaseTiler, ABC):
    """
    Легаси реализация тайлера для карт со старым форматом жсона
    (состоящим только из словаря тайлов)
    """
    @classmethod
    def _get_tiles(cls) -> dict:
        return cls._load_data()

    @classmethod
    def get_fill_cords(cls, tile_code: str) -> tuple[int, int]:
        tile = cls._get_tile(tile_code)
        x, y = tile.get("x"), tile.get("y")
        return x, y

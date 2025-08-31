from abc import ABC
from functools import cache
from json import load

from modules.roll.service.base.models.mapdata_things import MapData
from modules.roll.service.base.tiler.tilers.base_tiler import BaseTiler


class LegacyTiler(BaseTiler, ABC):
    """
    Легаси реализация тайлера для карт со старым форматом жсона
    (состоящим только из словаря тайлов)
    """
    @cache
    def _load_data(self) -> MapData:
        with self.data_path.open("r", encoding="utf-8") as data_file:
            data = load(data_file)
            return MapData(**{"tiles": {
                tile_id: {
                    "id": tile_id,
                    "fill_cords": (tile["x"], tile["y"]),
                    "routes": tile["routes"],
                }
                for tile_id, tile in data.items()
            }})

    def get_center_cords(self, tile_code: str) -> tuple[int, int]:
        return self.get_fill_cords(tile_code)

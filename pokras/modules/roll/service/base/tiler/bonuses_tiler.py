from abc import ABC

from modules.roll.service.base.tiler.base_tiler import BaseTiler


class BonusesTiler(BaseTiler, ABC):
    @classmethod
    def get_tile_bonus(cls, tile_code: str) -> int:
        bonuses = cls._load_data().get("tiles_bonuses", {})
        return bonuses.get(tile_code, 0)

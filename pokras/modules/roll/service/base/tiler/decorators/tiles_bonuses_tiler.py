from modules.roll.service.base.tiler.abc.tiler_decorator import TilerDecorator


class TilesBonusesTiler(TilerDecorator):
    def get_tile_bonus(self, tile_code: str) -> int:
        bonuses = self._load_data().tiles_bonuses
        return bonuses.get(tile_code, 0)

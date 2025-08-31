from modules.roll.service.base.tiler.abc.tiler_decorator import TilerDecorator


class SpawnProhibitedTiler(TilerDecorator):
    def can_spawn(self, tile_code: str) -> bool:
        tile = self._get_tile(tile_code)
        return tile.can_spawn

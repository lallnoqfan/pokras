from modules.roll.service.base.tiler.base_tiler import BaseTiler


class SpawnProhibitedTiler(BaseTiler):
    @classmethod
    def can_spawn(cls, tile_code: str) -> bool:
        tile = cls._get_tile(tile_code)
        return tile.get("can_spawn", True)

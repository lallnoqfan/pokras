from config import Paths
from game.games.base.tiler.legacy_tiler import LegacyTiler


class StalkerTiler(LegacyTiler):
    DATA_PATH = Paths.STALKER_TILES

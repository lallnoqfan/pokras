from config import Paths
from game.games.base.tiler.legacy_tiler import LegacyTiler


class EuClassicTiler(LegacyTiler):
    DATA_PATH = Paths.EU_CLASSIC_TILES

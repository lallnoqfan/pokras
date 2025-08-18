from config import Paths
from modules.roll.service.base.tiler.legacy_tiler import LegacyTiler


class EuClassicTiler(LegacyTiler):
    DATA_PATH = Paths.EU_CLASSIC_TILES

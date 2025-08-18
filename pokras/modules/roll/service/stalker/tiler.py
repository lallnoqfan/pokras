from config import Paths
from modules.roll.service.base.tiler.legacy_tiler import LegacyTiler


class StalkerTiler(LegacyTiler):
    DATA_PATH = Paths.STALKER_TILES

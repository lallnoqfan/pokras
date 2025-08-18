from config import Paths
from modules.roll.service.base.tiler.legacy_tiler import LegacyTiler


class KoreaTiler(LegacyTiler):
    DATA_PATH = Paths.KOREA_TILES

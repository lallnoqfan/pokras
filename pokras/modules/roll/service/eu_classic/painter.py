from config import Paths
from modules.roll.service.base.painter.base_painter import BasePainter


class EuClassicPainter(BasePainter):
    TILES_MAP = Paths.EU_CLASSIC_MAP

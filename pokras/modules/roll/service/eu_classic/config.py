from config import Paths
from modules.roll.service.base.models.config import ServiceConfig, PainterConfig, TilerConfig
from modules.roll.service.base.models.utils_things import Layer
from modules.roll.service.base.painter.base_painter import BasePainter
from modules.roll.service.base.tiler.tilers.legacy_tiler import LegacyTiler


class EuClassicPainterConfig(PainterConfig):
    base_painter = BasePainter
    map_layer = Layer(Paths.EU_CLASSIC / "map.png")


class EuClassicTilerConfig(TilerConfig):
    base_tiler = LegacyTiler
    data_path = Paths.EU_CLASSIC / "tiles_data.json"


class EuClassicConfig(ServiceConfig):
    painter_config = EuClassicPainterConfig
    tiler_config = EuClassicTilerConfig

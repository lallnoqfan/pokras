from config import Paths
from modules.roll.service.base.models.config import ServiceConfig, PainterConfig, TilerConfig
from modules.roll.service.base.models.utils_things import Layer
from modules.roll.service.base.painter.base_painter import BasePainter
from modules.roll.service.base.tiler.tilers.legacy_tiler import LegacyTiler


class StalkerPainterConfig(PainterConfig):
    base_painter = BasePainter
    map_layer = Layer(Paths.STALKER / "map.png")


class StalkerTilerConfig(TilerConfig):
    base_tiler = LegacyTiler
    data_path = Paths.STALKER / "tiles_data.json"


class StalkerConfig(ServiceConfig):
    painter_config = StalkerPainterConfig
    tiler_config = StalkerTilerConfig

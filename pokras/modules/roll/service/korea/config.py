from config import Paths
from modules.roll.service.base.models.config import ServiceConfig, PainterConfig, TilerConfig
from modules.roll.service.base.models.utils_things import Layer
from modules.roll.service.base.painter.base_painter import BasePainter
from modules.roll.service.base.tiler.tilers.legacy_tiler import LegacyTiler


class KoreaPainterConfig(PainterConfig):
    base_painter = BasePainter
    map_layer = Layer(Paths.KOREA / "map.png")


class KoreaTilerConfig(TilerConfig):
    base_tiler = LegacyTiler
    data_path = Paths.KOREA / "tiles_data.json"


class KoreaConfig(ServiceConfig):
    painter_config = KoreaPainterConfig
    tiler_config = KoreaTilerConfig

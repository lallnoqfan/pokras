from config import Paths
from modules.roll.service.base.models.config import ServiceConfig, PainterConfig, TilerConfig
from modules.roll.service.base.models.utils_things import Layer
from modules.roll.service.base.painter.base_painter import BasePainter
from modules.roll.service.base.tiler.tilers.base_tiler import BaseTiler


class SradtarcticaPainterConfig(PainterConfig):
    base_painter = BasePainter
    map_layer = Layer(Paths.SRADTARCTICA / "map.png")


class SradtarcticaTilerConfig(TilerConfig):
    base_tiler = BaseTiler
    data_path = Paths.SRADTARCTICA / "tiles_data.json"


class SradtarcticaConfig(ServiceConfig):
    # todo: add numerical parser
    painter_config = SradtarcticaPainterConfig
    tiler_config = SradtarcticaTilerConfig

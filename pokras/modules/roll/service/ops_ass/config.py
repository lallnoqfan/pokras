from config import Paths
from modules.roll.service.base.models.config import ServiceConfig, PainterConfig, TilerConfig
from modules.roll.service.base.models.utils_things import Layer
from modules.roll.service.base.painter.layered_painter import LayeredPainter
from modules.roll.service.base.tiler.tilers.base_tiler import BaseTiler


class OpsAssPainterConfig(PainterConfig):
    base_painter = LayeredPainter
    fg_layers = [Layer(Paths.OPS_ASS / "tiles_ids.png", (485, 16))]
    map_layer = Layer(Paths.OPS_ASS / "tiles_map.png", (461, 8))
    bg_layers = [Layer(Paths.OPS_ASS / "bg_rachnera.png", (0, 0))]


class OpsAssTilerConfig(TilerConfig):
    base_tiler = BaseTiler
    data_path = Paths.OPS_ASS / "tiles_data.json"


class OpsAssConfig(ServiceConfig):
    painter_config = OpsAssPainterConfig
    tiler_config = OpsAssTilerConfig

    use_tiles_aliases = True
    use_tiles_bonuses = True
    use_spawn_prohibited_tiles = True

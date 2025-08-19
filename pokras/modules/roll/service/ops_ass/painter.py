from config import Paths
from modules.roll.service.base.models.layer import Layer
from modules.roll.service.base.painter.layered_painter import LayeredPainter


class OpsAssPainter(LayeredPainter):
    FG_LAYERS = (Layer(Paths.OPS_ASS / "tiles_ids.png", (485, 16)), )
    TILES_MAP = Layer(Paths.OPS_ASS / "tiles_map.png", (461, 8))
    BG_LAYERS = (Layer(Paths.OPS_ASS / "bg_rachnera.png", (0, 0)),)

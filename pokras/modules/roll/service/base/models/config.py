from abc import ABC
from pathlib import Path
from typing import Type

from config import Paths
from modules.roll.service.base.models.utils_things import Layer
from modules.roll.service.base.painter.base_painter import BasePainter
from modules.roll.service.base.painter.layered_painter import LayeredPainter
from modules.roll.service.base.tiler.abc.tiler import Tiler


class PainterConfig(ABC):
    base_painter: Type[BasePainter | LayeredPainter]
    fg_layers: list[Layer] | None = None
    map_layer: Layer
    bg_layers: list[Layer] | None = None
    font_path: Path = Paths.FONT_CODENAME


class TilerConfig(ABC):
    base_tiler: Type[Tiler]
    data_path: Path


class ServiceConfig(ABC):
    painter_config: Type[PainterConfig]
    tiler_config: Type[TilerConfig]

    use_tiles_aliases: bool = False
    use_tiles_bonuses: bool = False
    use_spawn_prohibited_tiles: bool = False

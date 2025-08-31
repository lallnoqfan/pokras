from functools import cache
from pathlib import Path

from PIL import Image

from modules.roll.service.base.models.gamestate_things import CountryState
from modules.roll.service.base.painter.base_painter import BasePainter
from modules.roll.service.base.models.utils_things import Layer
from modules.roll.service.base.repository.repository import Repository
from modules.roll.service.base.tiler.abc.tiler import Tiler


class LayeredPainter(BasePainter):
    """
    ...
    """
    def __init__(self, font_path: Path, map_layer: Layer, bg_layers: list[Layer], fg_layers: list[Layer]):
        super().__init__(font_path, map_layer)
        self.bg_layers = bg_layers
        self.fg_layers = fg_layers

    @staticmethod
    @cache
    def _load_layer(layer: Layer) -> Image.Image:
        return Image.open(layer.file_path).convert("RGBA")

    def draw_map(self, countries: list[CountryState], tiler: Tiler, repository: Repository) -> Image.Image:
        map_image = self._load_layer(self.bg_layers[0]).copy()

        for bg_layer in self.bg_layers[1:]:
            layer_image = self._load_layer(bg_layer)
            map_image.paste(layer_image, box=bg_layer.paste_bias, mask=layer_image)

        tiles_image = super().draw_map(countries, tiler, repository)
        map_image.paste(tiles_image, box=self.map_layer.paste_bias, mask=tiles_image)

        for fg_layer in self.fg_layers:
            layer_image = self._load_layer(fg_layer)
            map_image.paste(layer_image, box=fg_layer.paste_bias, mask=layer_image)

        return map_image

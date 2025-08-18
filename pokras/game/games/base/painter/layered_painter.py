from abc import ABC
from functools import cache
from typing import ClassVar, Type

from PIL import Image

from game.games.base.painter.base_painter import BasePainter
from game.games.base.painter.country import Country
from game.games.base.painter.layer import Layer
from game.games.base.tiler.tiler import Tiler


class LayeredPainter(BasePainter, ABC):
    """
    ...
    """
    BG_LAYERS: ClassVar[tuple[Layer]]
    FG_LAYERS: ClassVar[tuple[Layer]]

    @classmethod
    @cache
    def _load_layer(cls, layer: Layer) -> Image.Image:
        return Image.open(layer.file_path).convert("RGBA")

    @classmethod
    def draw_map(cls, tiler: Type[Tiler], countries: list[Country]) -> Image.Image:
        map_image = cls._load_layer(cls.BG_LAYERS[0]).copy()

        for bg_layer in cls.BG_LAYERS[1:]:
            layer_image = cls._load_layer(bg_layer)
            map_image.paste(layer_image, box=bg_layer.paste_bias, mask=layer_image)

        tiles_image = super().draw_map(tiler, countries)
        map_image.paste(tiles_image, box=cls.TILES_MAP.paste_bias, mask=tiles_image)

        for fg_layer in cls.FG_LAYERS:
            layer_image = cls._load_layer(fg_layer)
            map_image.paste(layer_image, box=fg_layer.paste_bias, mask=layer_image)

        return map_image

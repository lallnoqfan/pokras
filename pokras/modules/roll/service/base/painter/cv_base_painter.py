from functools import cache
from pathlib import Path

import cv2
import numpy as np
from webcolors import hex_to_rgb

from modules.roll.service.base.models.gamestate_things import CountryState
from modules.roll.service.base.models.utils_things import Layer
from modules.roll.service.base.painter.base_painter import BasePainter
from modules.roll.service.base.repository.repository import Repository
from modules.roll.service.base.tiler.abc.tiler import Tiler
from utils.perf import method_performance


class Cv2BasePainter(BasePainter):
    @staticmethod
    @cache
    def _load_map(layer: Layer) -> np.ndarray:
        # Load the image as a 3-channel BGR image, discarding any alpha channel
        return cv2.imread(layer.file_path.__str__(), cv2.IMREAD_COLOR)

    @method_performance
    def draw_map(self, countries: list[CountryState], tiler: Tiler, repository: Repository) -> np.ndarray:
        # The image is guaranteed to be 3-channel BGR now
        map_image = self._load_map(self.map_layer).copy()

        h, w = map_image.shape[:2]
        mask = np.zeros((h + 2, w + 2), dtype=np.uint8)

        if isinstance(self.map_layer, Path):
            dx, dy = 0, 0
        else:
            dx, dy = self.map_layer.paste_bias

        for country in countries:
            for tile in repository.get_country_tiles(country):
                tile_code = tile.code
                x, y = tiler.get_fill_cords(tile_code)
                x, y = x - dx, y - dy

                fill_color = hex_to_rgb(country.color)[::-1]

                cv2.floodFill(map_image, mask, (x, y), fill_color)

        return map_image

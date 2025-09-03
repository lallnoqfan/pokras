from functools import cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from webcolors import hex_to_rgb

from modules.roll.service.base.models.gamestate_things import CountryState
from modules.roll.service.base.models.utils_things import Layer
from modules.roll.service.base.painter.painter import Painter
from modules.roll.service.base.repository.repository import Repository
from modules.roll.service.base.tiler.abc.tiler import Tiler
from utils.perf import method_performance


class BasePainter(Painter):
    """
    Базовая реализация покрасчика. Рисует карту без легенды.
    """
    def __init__(self, font_path: Path, map_layer: Layer):
        super().__init__(font_path, map_layer)

    @staticmethod
    @cache
    def _load_map(layer: Layer) -> Image.Image:
        return Image.open(layer.file_path).convert("RGBA")

    @method_performance
    def draw_map(self, countries: list[CountryState], tiler: Tiler, repository: Repository) -> Image.Image:
        map_image = self._load_map(self.map_layer).copy()

        if isinstance(self.map_layer, Path):
            dx, dy = 0, 0
        else:
            dx, dy = self.map_layer.paste_bias
        for country in countries:
            for tile in repository.get_country_tiles(country):
                tile_code = tile.code
                x, y = tiler.get_fill_cords(tile_code)
                x, y = x - dx, y - dy
                ImageDraw.floodfill(map_image, (x, y), (*hex_to_rgb(country.color), 255))

        return map_image

    def _draw_country_title(self, country_name: str, hex_color: str = "#000000", skip_key: bool = False) -> Image.Image:
        w, h = 960, 50
        img = Image.new("RGB", (w, h), (255, 255, 255))

        if not skip_key:
            ImageDraw.Draw(img).rectangle(
                xy=((5, 5), (45, 45)),
                fill=hex_to_rgb(hex_color),
                outline=(0, 0, 0),
                width=5,
            )

        ImageDraw.Draw(img).text(
            xy=(55 if not skip_key else 10, 0),
            text=country_name,
            fill=(0, 0, 0),
            font=ImageFont.truetype(self.font_path, 40, encoding="unic"),
        )

        return img

    @method_performance
    def draw_legend(self, countries: list[CountryState], tiler: Tiler, repository: Repository) -> Image.Image:
        active_countries = {
            country.color: country.name
            for country in countries
            if repository.get_country_tiles(country)
        }
        non_active_countries = {
            country.color: country.name
            for country in countries
            if country.color not in active_countries
        }

        active_countries_exists = len(active_countries) > 0
        non_active_countries_exists = len(non_active_countries) > 0
        active_non_active_exists = active_countries_exists and non_active_countries_exists

        w, h = 960, 50 * (
                len(active_countries) + len(non_active_countries) +
                active_countries_exists + non_active_countries_exists + active_non_active_exists
        )

        img = Image.new("RGB", (w, h), (255, 255, 255))

        i = 0

        if active_countries_exists:
            title_img = self._draw_country_title("Активные:", skip_key=True)
            img.paste(title_img, (0, i * 50))
            i += 1

        for color, name in active_countries.items():
            title_img = self._draw_country_title(name, color)
            img.paste(title_img, (0, i * 50))
            i += 1

        if active_non_active_exists:
            i += 1

        if non_active_countries_exists:
            title_img = self._draw_country_title("Без территорий:", skip_key=True)
            img.paste(title_img, (0, i * 50))
            i += 1

        for color, name in non_active_countries.items():
            title_img = self._draw_country_title(name, color)
            img.paste(title_img, (0, i * 50))
            i += 1

        return img

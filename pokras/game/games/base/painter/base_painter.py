from abc import ABC
from functools import cache
from pathlib import Path
from typing import Type

from PIL import Image, ImageDraw, ImageFont
from webcolors import hex_to_rgb

from config import Paths
from game.games.base.painter.country import Country
from game.games.base.painter.painter import Painter
from game.games.base.tiler.tiler import Tiler


class BasePainter(Painter, ABC):
    """
    Базовая реализация покрасчика. Рисует карту без легенды.
    """
    FONT = Paths.FONT_CODENAME

    @classmethod
    @cache
    def _load_map(cls) -> Image.Image:
        if isinstance(cls.TILES_MAP, Path):
            return Image.open(cls.TILES_MAP).convert("RGBA")
        return Image.open(cls.TILES_MAP.file_path).convert("RGBA")

    @classmethod
    def draw_map(cls, tiler: Type[Tiler], countries: list[Country]) -> Image.Image:
        map_image = cls._load_map().copy()

        if isinstance(cls.TILES_MAP, Path):
            dx, dy = 0, 0
        else:
            dx, dy = cls.TILES_MAP.paste_bias
        for player in countries:
            for tile_code in player.tiles:
                x, y = tiler.get_fill_cords(tile_code)
                x, y = x - dx, y - dy
                ImageDraw.floodfill(map_image, (x, y), (*hex_to_rgb(player.hex_color), 255))

        return map_image

    @classmethod
    def _draw_country_title(cls, country_name: str, hex_color: str = "#000000", skip_key: bool = False) -> Image.Image:
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
            font=ImageFont.truetype(cls.FONT, 40, encoding="unic"),
        )

        return img

    @classmethod
    def draw_legend(cls, tiler: Type[Tiler], countries: list[Country]) -> Image.Image:
        active_countries = {
            player.hex_color: player.name
            for player in countries
            if player.tiles
        }
        non_active_countries = {
            player.hex_color: player.name
            for player in countries
            if not player.tiles
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
            title_img = cls._draw_country_title("Активные:", skip_key=True)
            img.paste(title_img, (0, i * 50))
            i += 1

        for key in active_countries:
            title_img = cls._draw_country_title(active_countries[key], key)
            img.paste(title_img, (0, i * 50))
            i += 1

        if active_non_active_exists:
            i += 1

        if non_active_countries_exists:
            title_img = cls._draw_country_title("Без территорий:", skip_key=True)
            img.paste(title_img, (0, i * 50))
            i += 1

        for key in non_active_countries:
            title_img = cls._draw_country_title(non_active_countries[key], key)
            img.paste(title_img, (0, i * 50))
            i += 1

        return img

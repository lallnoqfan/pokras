from dataclasses import dataclass, field
from functools import cache
from json import load

from PIL import Image, ImageDraw, ImageFont
from webcolors import hex_to_rgb

from config import Paths, AppConfig


@dataclass
class CountryModel:
    """
    Моделька страны, используемая для рендера карты и легенды.

    Attributes:
        name: Название страны
        hex_color: Цвет страны в HEX формате
        tiles: Список кодов тайлов, которые принадлежат данной стране
    """
    name: str
    hex_color: str
    tiles: list[str] = field(default_factory=lambda: [])


class ResourcesHandler:

    @staticmethod
    @cache
    def load_tiles_data() -> dict:
        with Paths.TILES_DATA.open("r", encoding="utf-8") as tiles_data:
            return load(tiles_data)

    @staticmethod
    @cache
    def load_map() -> Image.Image:
        return Image.open(Paths.MAP).convert('RGB')

    @classmethod
    def load_rules(cls) -> str:
        with Paths.RULES.open("r", encoding="utf-8") as rules:
            return rules.read()

    @classmethod
    def get_tile(cls, tile_id: str) -> dict | None:
        return cls.load_tiles_data().get(tile_id, None)

    @classmethod
    def tile_exists(cls, tile_id: str) -> bool:
        return tile_id in cls.load_tiles_data()

    @classmethod
    def draw_map(cls, countries: list[CountryModel]) -> Image.Image:
        map_image = cls.load_map().copy()

        for player in countries:
            for tile in player.tiles:
                tile = cls.get_tile(tile)
                if not tile:
                    continue
                xy = (tile.get('x'), tile.get('y'))
                ImageDraw.floodfill(map_image, xy, hex_to_rgb(player.hex_color))

        return map_image

    @classmethod
    def _draw_country_title(cls, country_name: str, hex_color: str, skip_key: bool = False) -> Image.Image:
        w, h = 960, 50
        img = Image.new('RGB', (w, h), (255, 255, 255))

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
            font=ImageFont.truetype(Paths.FONT, 40, encoding='unic'),
        )

        return img

    @classmethod
    def draw_countries(cls, countries: list[CountryModel]) -> Image.Image:

        if AppConfig.DEBUG:
            for country in countries:
                print(country)

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

        w, h = 960, 50 * (
                len(active_countries) + len(non_active_countries) +
                (len(active_countries) > 0) + (len(non_active_countries) > 0) +
                (len(active_countries) > 0 and len(non_active_countries) > 0)
        )
        img = Image.new('RGB', (w, h), (255, 255, 255))

        i = 0
        if len(active_countries) > 0:
            title_img = cls._draw_country_title("Active:", "#000000", skip_key=True)
            img.paste(title_img, (0, i * 50))
            i += 1

        for key in active_countries:
            title_img = cls._draw_country_title(active_countries[key], key)
            img.paste(title_img, (0, i * 50))
            i += 1

        i += 1
        if len(non_active_countries) > 0:
            title_img = cls._draw_country_title("Inactive:", "#000000", skip_key=True)
            img.paste(title_img, (0, i * 50))
            i += 1

        for key in non_active_countries:
            title_img = cls._draw_country_title(non_active_countries[key], key)
            img.paste(title_img, (0, i * 50))
            i += 1

        return img

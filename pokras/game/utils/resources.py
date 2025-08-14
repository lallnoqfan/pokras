from dataclasses import dataclass, field
from functools import cache
from json import load
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from webcolors import hex_to_rgb

from config import Paths, AppConfig
from game.tables.choices.game_map import GameMap


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

    _TILES_PATH: Path = Paths.EU_CLASSIC_TILES
    _MAP_PATH: Path = Paths.EU_CLASSIC_MAP
    _FONT = Paths.FONT_CODENAME

    def __new__(cls, game_map: GameMap):
        match game_map:
            case GameMap.eu_classic:
                return EuClassicResources
            case GameMap.stalker:
                return StalkerResources
            case GameMap.korea:
                return KoreaResources

    @classmethod
    @cache
    def load_tiles_data(cls) -> dict:
        with cls._TILES_PATH.open("r", encoding="utf-8") as tiles_data:
            return load(tiles_data)

    @classmethod
    @cache
    def load_map(cls) -> Image.Image:
        return Image.open(cls._MAP_PATH).convert('RGB')

    @classmethod
    def get_tile(cls, tile_id: str) -> dict | None:
        return cls.load_tiles_data().get(tile_id, None)

    @classmethod
    def get_adjacent_tiles(cls, tile_id: str) -> list[str]:
        tile = cls.get_tile(tile_id)
        if not tile:
            return []
        return tile.get("routes", [])

    @classmethod
    def tile_exists(cls, tile_id: str) -> bool:
        print(tile_id)
        return tile_id in cls.load_tiles_data()

    @classmethod
    def calc_distance(cls, first_tile_id: str, second_tile_id: str) -> float:
        first_tile = cls.get_tile(first_tile_id)
        second_tile = cls.get_tile(second_tile_id)

        x1, y1 = first_tile.get('x'), first_tile.get('y')
        x2, y2 = second_tile.get('x'), second_tile.get('y')

        distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        print("=" * 50)
        print(first_tile_id, second_tile_id)
        print((x1, y1), (x2, y2))
        print(distance)
        print("=" * 50)

        return distance

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
            font=ImageFont.truetype(cls._FONT, 40, encoding='unic'),
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

        active_countries_exists = len(active_countries) > 0
        non_active_countries_exists = len(non_active_countries) > 0
        active_non_active_exists = active_countries_exists and non_active_countries_exists

        w, h = 960, 50 * (
                len(active_countries) + len(non_active_countries) +
                active_countries_exists + non_active_countries_exists + active_non_active_exists
        )

        img = Image.new('RGB', (w, h), (255, 255, 255))

        i = 0

        if active_countries_exists:
            title_img = cls._draw_country_title("Active:", "#000000", skip_key=True)
            img.paste(title_img, (0, i * 50))
            i += 1

        for key in active_countries:
            title_img = cls._draw_country_title(active_countries[key], key)
            img.paste(title_img, (0, i * 50))
            i += 1

        if active_non_active_exists:
            i += 1

        if non_active_countries_exists:
            title_img = cls._draw_country_title("Inactive:", "#000000", skip_key=True)
            img.paste(title_img, (0, i * 50))
            i += 1

        for key in non_active_countries:
            title_img = cls._draw_country_title(non_active_countries[key], key)
            img.paste(title_img, (0, i * 50))
            i += 1

        return img


class EuClassicResources(ResourcesHandler):
    ...


class StalkerResources(ResourcesHandler):
    _TILES_PATH: Path = Paths.STALKER_TILES
    _MAP_PATH: Path = Paths.STALKER_MAP


class KoreaResources(ResourcesHandler):
    _TILES_PATH: Path = Paths.KOREA_TILES
    _MAP_PATH: Path = Paths.KOREA_MAP

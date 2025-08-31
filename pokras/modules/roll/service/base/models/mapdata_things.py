from typing import FrozenSet

from pydantic import BaseModel


class MapData(BaseModel):
    """
    Информация о карте.

    Attributes:
        version: версия схемы
        tiles: словарь тайлов
        tiles_aliases: алиасы тайлов
        tiles_bonuses: бонусы тайлов
        regions: словарь регионов
        regions_aliases: алиасы регионов
        regions_bonuses: бонусы регионов
    """
    tiles: dict[str, "TileSchema"]
    version: str | None = None
    tiles_aliases: dict[str, str] | None = None
    tiles_bonuses: dict[str, int] | None = None
    regions: dict[str, "RegionSchema"] | None = None
    regions_aliases: dict[str, str] | None = None
    regions_bonuses: dict[str, int] | None = None


class TileSchema(BaseModel):
    """
    Схема тайла.

    Attributes:
        id: код тайла
        fill_cords: координаты заливки
        center_cords: приблизительные координаты центра
        routes: коды соседних тайлов
    """
    id: str
    fill_cords: tuple[int, int]
    center_cords: tuple[int, int] | None = None
    routes: FrozenSet[str]
    can_spawn: bool = True


class RegionSchema(BaseModel):
    """
    Схема региона.

    Attributes:
        id: название региона
        tiles: список тайлов, принадлежащих региону
    """
    id: str
    tiles: FrozenSet[str]

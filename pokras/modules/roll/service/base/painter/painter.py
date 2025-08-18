from abc import ABC, abstractmethod
from pathlib import Path
from typing import ClassVar, Type

from PIL import Image

from modules.country.models.country import Country
from modules.roll.service.base.painter.layer import Layer
from modules.roll.service.base.tiler.tiler import Tiler


class Painter(ABC):
    """
    Абстрактный класс-покрасчик, отвечающий за отрисовку карты и легенды.

    Attributes:
        FONT: Путь к шрифту, которым рисуется легенда
        TILES_MAP: Путь к файлу карты
    """
    FONT: ClassVar[Path]
    TILES_MAP: ClassVar[Layer]

    @classmethod
    @abstractmethod
    def draw_map(cls, tiler: Type[Tiler], countries: list[Country]) -> Image.Image:
        """
        Отрисовка карты.

        Args:
            tiler: Тайлер, из которого получаем информацию о тайлах
            countries: Список моделек стран

        Returns:
            Отрисованная карта
        """
        ...

    @classmethod
    @abstractmethod
    def draw_legend(cls, tiler: Type[Tiler], countries: list[Country]) -> Image.Image:
        """
        Отрисовка легенды.

        Args:
            tiler: Тайлер, из которого получаем информацию о тайлах.
                   Используется для карт, легенда которых зависит от состояния игры.
            countries: Список моделек стран

        Returns:
            Отрисованная легенда
        """
        ...

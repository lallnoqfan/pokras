from abc import ABC, abstractmethod
from pathlib import Path

from PIL import Image

from modules.roll.service.base.models.gamestate_things import CountryState
from modules.roll.service.base.models.utils_things import Layer
from modules.roll.service.base.repository.repository import Repository
from modules.roll.service.base.tiler.abc.tiler import Tiler


class Painter(ABC):
    """
    Абстрактный класс-покрасчик, отвечающий за отрисовку карты и легенды.

    Args:
        font_path: Путь к шрифту, которым рисуется легенда
        map_layer: Слой карты
    """
    def __init__(self, font_path: Path, map_layer: Layer):
        self.font_path = font_path
        self.map_layer = map_layer

    @abstractmethod
    def draw_map(self, countries: list[CountryState], tiler: Tiler, repository: Repository) -> Image.Image:
        """
        Отрисовка карты.

        Args:
            tiler: Тайлер, из которого получаем информацию о тайлах
            repository: Репозиторий, из которого берём состояние игры
            countries: Список моделек стран

        Returns:
            Отрисованная карта
        """

    @abstractmethod
    def draw_legend(self, countries: list[CountryState], tiler: Tiler, repository: Repository) -> Image.Image:
        """
        Отрисовка легенды.

        Args:
            tiler: Тайлер, из которого получаем информацию о тайлах
            repository: Репозиторий, из которого берём состояние игры.
                   Используется для карт, легенда которых зависит от состояния игры.
            countries: Список моделек стран

        Returns:
            Отрисованная легенда
        """

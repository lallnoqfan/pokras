from abc import ABC, abstractmethod
from pathlib import Path

from modules.roll.service.base.models.mapdata_things import MapData, TileSchema


class Tiler(ABC):
    """
    Абстрактный класс, отвечающий за чтение информации о карте из жсончика.
    Прячет внутри себя весь не обёрнутый в модельки доступ к словарям по строковым ключам.

    Args:
        data_path: Путь к файлу с информацией о карте
    """
    def __init__(self, data_path: Path):
        self.data_path = data_path

    @abstractmethod
    def _load_data(self) -> MapData:
        """
        Загружает жсон с информацией о карте

        Returns:
            Словарик с информацией о карте
        """

    @abstractmethod
    def _get_tiles(self) -> dict[str, TileSchema]:
        """
        Из исходного жсона выбирает словарик с информацией о тайлах

        Returns:
            Словарик с информацией о тайлах
        """

    @abstractmethod
    def _get_tile(self, tile_code: str) -> TileSchema | None:
        """
        Возвращает тайл по его коду

        Args:
             tile_code: Код тайла

        Returns:
            Моделька тайла, если тайл существует
        """

    @abstractmethod
    def get_by_alias(self, alias: str) -> str:
        return alias

    @abstractmethod
    def get_fill_cords(self, tile_code: str) -> tuple[int, int]:
        """
        Возвращает координаты точки заливки тайла. Имплаит, что код тайла валидный.

        Args:
            tile_code: Код тайла

        Returns:
            Координаты точки заливки
        """

    @abstractmethod
    def get_center_cords(self, tile_code: str) -> tuple[int, int]:
        """
        Возвращает координаты центра тайла. Имплаит, что код тайла валидный.

        Args:
            tile_code: Код тайла

        Returns:
            Координаты центра тайла
        """

    @abstractmethod
    def get_adjacent_tiles(self, tile_code: str) -> frozenset[str]:
        """
        Возвращает список кодов соседних тайлов. Имплаит, что код тайла валидный.

        Args:
            tile_code: Код тайла

        Returns:
            Список кодов соседних тайлов
        """

    @abstractmethod
    def get_tile_bonus(self, tile_code: str) -> int:
        ...

    @abstractmethod
    def tile_exists(self, tile_code: str) -> bool:
        """
        Проверяет, существует ли тайл с указанным кодом

        Args:
            tile_code: Код тайла

        Returns:
            True, если тайл существует
        """

    @abstractmethod
    def can_spawn(self, tile_code: str) -> bool:
        """
        Проверяет, разрешён ли спавн новой страны на тайле с указанным кодом.

        Args:
            tile_code: Код тайла

        Returns:
            True, если спавн разрешён
        """

    @abstractmethod
    def calc_distance(self, first_tile_code: str, second_tile_code: str) -> float:
        """
        Расчёт расстояния между двумя тайлами. Имплаит, что оба кода тайлов валидные.

        Args:
            first_tile_code: Код первого тайла
            second_tile_code: Код второго тайла

        Returns:
            Расстояние (в пикселях) между тайлами
        """

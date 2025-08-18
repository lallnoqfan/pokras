from abc import ABC, abstractmethod
from pathlib import Path
from typing import ClassVar


class Tiler(ABC):
    """
    Абстрактный класс, отвечающий за чтение информации о карте из жсончика.
    Прячет внутри себя весь не обёрнутый в модельки доступ к словарям по строковым ключам.

    Attributes:
        DATA_PATH: Путь к файлу с информацией о карте
    """
    DATA_PATH: ClassVar[Path]

    @classmethod
    @abstractmethod
    def _load_data(cls) -> dict:
        """
        Загружает жсон с информацией о карте

        Returns:
            Словарик с информацией о карте
        """
        ...

    @classmethod
    @abstractmethod
    def _get_tiles(cls) -> dict:
        """
        Из исходного жсона выбирает словарик с информацией о тайлах

        Returns:
            Словарик с информацией о тайлах
        """
        ...

    @classmethod
    @abstractmethod
    def _get_tile(cls, tile_code: str) -> dict | None:
        """
        Возвращает тайл по его коду

        Args:
             tile_code: Код тайла

        Returns:
            Моделька тайла, если тайл существует
        """
        ...

    @classmethod
    @abstractmethod
    def tile_exists(cls, tile_code: str) -> bool:
        """
        Проверяет, существует ли тайл с указанным кодом

        Args:
            tile_code: Код тайла

        Returns:
            True, если тайл существует
        """
        ...

    @classmethod
    @abstractmethod
    def get_fill_cords(cls, tile_code: str) -> tuple[int, int]:
        """
        Возвращает координаты точки заливки тайла. Имплаит, что код тайла валидный.

        Args:
            tile_code: Код тайла

        Returns:
            Координаты точки заливки
        """

    @classmethod
    @abstractmethod
    def get_adjacent_tiles(cls, tile_code: str) -> list[str]:
        """
        Возвращает список кодов соседних тайлов. Имплаит, что код тайла валидный.

        Args:
            tile_code: Код тайла

        Returns:
            Список кодов соседних тайлов
        """
        ...

    @classmethod
    @abstractmethod
    def calc_distance(cls, first_tile_code: str, second_tile_code: str) -> float:
        """
        Расчёт расстояния между двумя тайлами. Имплаит, что оба кода тайлов валидные.

        Args:
            first_tile_code: Код первого тайла
            second_tile_code: Код второго тайла

        Returns:
            Расстояние (в пикселях) между тайлами
        """
        ...

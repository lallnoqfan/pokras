from abc import ABC, abstractmethod
from typing import Type

from game.games.base.tiler.tiler import Tiler


class Parser(ABC):
    @classmethod
    @abstractmethod
    def parse_tiles(cls, tiler: Type[Tiler], tiles: str | list[str]) -> list[str]:
        """
        Tiles list normalization.
        """
        ...

    @classmethod
    @abstractmethod
    def get_roll_value(cls, roll: str | int | list[int]) -> int:
        ...

from abc import ABC, abstractmethod
from typing import Type

from modules.game.service.models.roll_values import RollValues
from modules.roll.service.base.tiler.tiler import Tiler


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
    def get_roll_value(cls, roll: str | int | list[int], roll_values: RollValues) -> int:
        ...

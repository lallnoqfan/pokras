from abc import ABC, abstractmethod

from modules.game.service.models.roll_values import RollValues
from modules.roll.service.base.tiler.abc.tiler import Tiler


class Parser(ABC):
    @abstractmethod
    def parse_tiles(self, tiler: Tiler, tiles: list[str]) -> list[str]:
        """
        Tiles list normalization.
        """
        ...

    @abstractmethod
    def get_roll_value(self, roll: str | int | list[int], roll_values: RollValues) -> int:
        ...

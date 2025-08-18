from abc import ABC, abstractmethod
from typing import ClassVar, Type

from modules.country.models.country import Country
from modules.game.models.game import Game
from modules.roll.service.base.painter.painter import Painter
from modules.roll.service.base.parser.parser import Parser
from modules.roll.service.base.repository.repository import Repository
from modules.roll.service.base.tiler.tiler import Tiler


class Service(ABC):
    """
    Абстрактный класс, отвечающий за логику покраса карты
    """
    tiler: ClassVar[Type[Tiler]]
    painter: ClassVar[Type[Painter]]
    repository: ClassVar[Type[Repository]]
    parser: ClassVar[Type[Parser]]

    @classmethod
    @abstractmethod
    def add_tiles(cls, game: Game, country: Country, roll: list[int], tiles: str | list[str]) -> tuple[bool, list[str]]:
        ...

    @classmethod
    @abstractmethod
    def add_expansion(cls, game: Game, country: Country, roll: list[int]) -> tuple[bool, list[str]]:
        ...

    @classmethod
    @abstractmethod
    def add_against(cls, game: Game, country: Country, target: Country, roll: list[int]) -> tuple[bool, list[str]]:
        ...

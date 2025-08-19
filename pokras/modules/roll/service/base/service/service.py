from abc import ABC, abstractmethod
from typing import ClassVar, Type

from modules.country.models.country import Country
from modules.game.models.game import Game
from modules.roll.service.base.models.prompt import Prompt
from modules.roll.service.base.models.roll_response import RollResponse
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
    def add_tiles(cls, game: Game, country: Country, prompt: Prompt, tiles: str | list[str]) -> RollResponse:
        ...

    @classmethod
    @abstractmethod
    def add_expansion(cls, game: Game, country: Country, prompt: Prompt) -> RollResponse:
        ...

    @classmethod
    @abstractmethod
    def add_against(cls, game: Game, country: Country, prompt: Prompt, target: Country) -> RollResponse:
        ...

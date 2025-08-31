from abc import ABC, abstractmethod

from modules.roll.service.base.models.api_things import TilesRollPrompt, ExpansionRollPrompt, AgainstRollPrompt, \
    RollResponse
from modules.roll.service.base.models.gamestate_things import GameState
from modules.roll.service.base.painter.painter import Painter
from modules.roll.service.base.parser.parser import Parser
from modules.roll.service.base.repository.repository import Repository
from modules.roll.service.base.tiler.abc.tiler import Tiler


class Service(ABC):
    """
    Абстрактный класс, отвечающий за логику покраса карты
    """
    def __init__(self, tiler: Tiler, painter: Painter, repository: Repository, parser: Parser):
        self.tiler = tiler
        self.painter = painter
        self.repository = repository
        self.parser = parser

    @abstractmethod
    def add_tiles(self, game: GameState, prompt: TilesRollPrompt) -> RollResponse:
        ...

    @abstractmethod
    def add_expansion(self, game: GameState, prompt: ExpansionRollPrompt) -> RollResponse:
        ...

    @abstractmethod
    def add_against(self, game: GameState, prompt: AgainstRollPrompt) -> RollResponse:
        ...

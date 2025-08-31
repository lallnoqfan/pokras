from abc import ABC

from modules.roll.service.base.models.api_things import RollResponse, TilesRollPrompt, ExpansionRollPrompt, \
    AgainstRollPrompt
from modules.roll.service.base.models.gamestate_things import GameState
from modules.roll.service.base.service.abc.service import Service


class ServiceDecorator(Service, ABC):
    """
    Абстрактный класс-декоратор, расширяющий поведение базового сервиса.

    Args:
        service: Базовый сервис
    """
    def __init__(self, service: Service):
        super().__init__(service.tiler, service.painter, service.repository, service.parser)
        self._service = service

    def add_tiles(self, game: GameState, prompt: TilesRollPrompt) -> RollResponse:
        return self._service.add_tiles(game, prompt)

    def add_expansion(self, game: GameState, prompt: ExpansionRollPrompt) -> RollResponse:
        return self._service.add_expansion(game, prompt)

    def add_against(self, game: GameState, prompt: AgainstRollPrompt) -> RollResponse:
        return self._service.add_against(game, prompt)

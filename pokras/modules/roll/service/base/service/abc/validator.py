from abc import ABC, abstractmethod

from modules.roll.service.base.models.api_things import TilesRollPrompt, RollResponse, ExpansionRollPrompt, \
    AgainstRollPrompt
from modules.roll.service.base.models.gamestate_things import GameState
from modules.roll.service.base.service.abc.service_decorator import ServiceDecorator


class Validator(ServiceDecorator, ABC):
    @abstractmethod
    def validate_tiles(self, game: GameState, prompt: TilesRollPrompt) -> RollResponse | None:
        ...

    @abstractmethod
    def validate_expansion(self, game: GameState, prompt: ExpansionRollPrompt) -> RollResponse | None:
        ...

    @abstractmethod
    def validate_against(self, game: GameState, prompt: AgainstRollPrompt) -> RollResponse | None:
        ...

    def add_tiles(self, game: GameState, prompt: TilesRollPrompt) -> RollResponse:
        response = self.validate_tiles(game, prompt)
        if response is not None:
            return response
        return self._service.add_tiles(game, prompt)

    def add_expansion(self, game: GameState, prompt: ExpansionRollPrompt) -> RollResponse:
        response = self.validate_expansion(game, prompt)
        if response is not None:
            return response
        return self._service.add_expansion(game, prompt)

    def add_against(self, game: GameState, prompt: AgainstRollPrompt) -> RollResponse:
        response = self.validate_against(game, prompt)
        if response is not None:
            return response
        return self._service.add_against(game, prompt)

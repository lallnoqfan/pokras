from abc import ABC, abstractmethod

from modules.roll.service.base.models.api_things import RollPrompt
from modules.roll.service.base.models.gamestate_things import GameState, CountryState
from modules.roll.service.base.service.abc.service_decorator import ServiceDecorator


class BonusProcessor(ServiceDecorator, ABC):
    @abstractmethod
    def process_bonus(self, game: GameState, country: CountryState, prompt: RollPrompt) -> tuple[int, str]:
        ...

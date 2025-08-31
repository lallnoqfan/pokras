from datetime import timedelta
from math import ceil
from typing import Callable

from modules.roll.service.base.models.api_things import RollPrompt, ExpansionRollPrompt, \
    AgainstRollPrompt, TilesRollPrompt, RollResponse
from modules.roll.service.base.models.gamestate_things import GameState
from modules.roll.service.base.service.abc.service import Service

from modules.roll.service.base.service.abc.service_decorator import ServiceDecorator
from modules.roll.service.base.service.abc.validator import Validator
from utils.text import Tags as T


class Cooler(ServiceDecorator):
    """
    Проверяет кд с последнего поста, прежде чем идти вниз по пайплайну.
    Подсасывается к валидатору, чтобы в случае фейла валидации передать "вы можете роллить снова".
    """
    def __init__(self, service: Service, validator: Validator):
        super().__init__(service)
        self._service = service
        self._validator = validator

    def __check_cooldown(self, game: GameState, prompt: RollPrompt, func: Callable[[], RollResponse]) -> RollResponse:
        country = self.repository.get_country_by_name(game, prompt.country)
        last_roll = self.repository.get_last_roll(game, country)
        if last_roll is None:
            self.repository.set_last_roll(game, country, prompt.timestamp)
            return func()

        zero = timedelta(seconds=0)
        time_since_last_roll = prompt.timestamp - last_roll.timestamp
        remaining_cooldown = game.cooldown - time_since_last_roll

        if remaining_cooldown <= zero:
            self.repository.set_last_roll(game, country, prompt.timestamp)
            return func()

        seconds_left = ceil(remaining_cooldown.total_seconds())
        # todo: move to responses
        response = [f"You only can roll again in {seconds_left} second{'s' if seconds_left != 1 else ''}"]

        return RollResponse(ok=False, map_state_changed=False, messages=response)

    def add_tiles(self, game: GameState, prompt: TilesRollPrompt) -> RollResponse:
        response = self._validator.validate_tiles(game, prompt)
        if response is not None:
            response.messages.append(T.spoiler("roll was not counted and you can roll again"))
            return response

        return self.__check_cooldown(game, prompt, lambda: self._service.add_tiles(game, prompt))

    def add_expansion(self, game: GameState, prompt: ExpansionRollPrompt) -> RollResponse:
        response = self._validator.validate_expansion(game, prompt)
        if response is not None:
            response.messages.append(T.spoiler("roll was not counted and you can roll again"))
            return response

        return self.__check_cooldown(game, prompt, lambda: self._service.add_expansion(game, prompt))

    def add_against(self, game: GameState, prompt: AgainstRollPrompt) -> RollResponse:
        response = self._validator.validate_against(game, prompt)
        if response is not None:
            response.messages.append(T.spoiler("roll was not counted and you can roll again"))
            return response

        return self.__check_cooldown(game, prompt, lambda: self._service.add_against(game, prompt))

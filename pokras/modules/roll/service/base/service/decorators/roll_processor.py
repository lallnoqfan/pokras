from typing import Callable

from modules.roll.responses import RollResponses
from modules.roll.service.base.models.api_things import TilesRollPrompt, RollResponse, ExpansionRollPrompt, \
    AgainstRollPrompt, RollPrompt
from modules.roll.service.base.models.gamestate_things import GameState
from modules.roll.service.base.service.abc.bonus_processor import BonusProcessor
from modules.roll.service.base.service.abc.service import Service
from modules.roll.service.base.service.abc.service_decorator import ServiceDecorator
from utils.perf import method_performance


class RollProcessor(ServiceDecorator):
    """
    Считает захваты от ролла и бонусов.

    *Прерывает исполнение, если ролл ПЛЮС бонусы не принесли захватов.*
    """
    def __init__(self, service: Service, bonus_processors: list[BonusProcessor]):
        super().__init__(service)
        self._bonus_processors = bonus_processors

    def _parse_roll_value(self, game: GameState, prompt: RollPrompt, response: list[str]) -> None:
        roll = prompt.roll
        roll_values = self.repository.get_roll_values(game)
        prompt.roll_value = self.parser.get_roll_value(roll, roll_values)
        response.append(RollResponses.roll(roll, prompt.roll_value))

    def _parse_bonuses(self, game: GameState, prompt: RollPrompt, response: list[str]) -> None:
        if not self._bonus_processors:
            return

        country = self.repository.get_country_by_name(game, prompt.country)

        for bonus_processor in self._bonus_processors:
            bonus, message = bonus_processor.process_bonus(game, country, prompt)
            if bonus > 0:
                prompt.roll_value += bonus
                response.append(message)

    def _process_roll(self, game: GameState, prompt: RollPrompt, func: Callable[[], RollResponse]) -> RollResponse:
        response = []
        self._parse_roll_value(game, prompt, response)
        self._parse_bonuses(game, prompt, response)

        if prompt.roll_value <= 0:
            return RollResponse(ok=True, map_state_changed=False, messages=response)

        service_response = func()
        if service_response.ok:
            response.extend(service_response.messages)
            service_response.messages = response
        return service_response

    @method_performance
    def add_tiles(self, game: GameState, prompt: TilesRollPrompt) -> RollResponse:
        return self._process_roll(game, prompt, lambda: self._service.add_tiles(game, prompt))

    @method_performance
    def add_expansion(self, game: GameState, prompt: ExpansionRollPrompt) -> RollResponse:
        return self._process_roll(game, prompt, lambda: self._service.add_expansion(game, prompt))

    @method_performance
    def add_against(self, game: GameState, prompt: AgainstRollPrompt) -> RollResponse:
        return self._process_roll(game, prompt, lambda: self._service.add_against(game, prompt))


class HardRollProcessor(RollProcessor):
    """
    Считает захваты от ролла и бонусов.

    *Прерывает исполнение, если ролл не принёс захватов.*
    """
    # basically, it is a dummy way to calculate bonuses for ops_ass map - ones that provide bonus on double+
    # once i feel for it may add complex bonuses (ones triggered on specific roll types only)
    def _process_roll(self, game: GameState, prompt: RollPrompt, func: Callable[[], RollResponse]) -> RollResponse:
        response = []
        self._parse_roll_value(game, prompt, response)

        if prompt.roll_value <= 0:
            return RollResponse(ok=True, map_state_changed=False, messages=response)

        self._parse_bonuses(game, prompt, response)

        service_response = func()
        if service_response.ok:
            response.extend(service_response.messages)
            service_response.messages = response
        return service_response

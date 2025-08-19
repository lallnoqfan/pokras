from datetime import timedelta
from math import ceil
from typing import Callable

from modules.country.models.country import Country
from modules.game.models.game import Game
from modules.roll.service.base.models.prompt import Prompt
from modules.roll.service.base.models.roll_response import RollResponse

from modules.roll.service.base.service.service import Service


class CooldownService(Service):
    def __init__(self, base_service: Service) -> None:
        self._base = base_service
        self.repository = base_service.repository  # noqa
        self.parser = base_service.parser          # noqa
        self.tiler = base_service.tiler            # noqa
        self.painter = base_service.painter        # noqa

    def _check_cooldown(self, game: Game, country: Country, prompt: Prompt,
                        func: Callable[[], RollResponse]) -> RollResponse:
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

        seconds_left = ceil(remaining_cooldown .total_seconds())
        messages = [f"You only can roll again in {seconds_left} second{'s' if seconds_left != 1 else ''}"]

        return RollResponse(ok=False, map_state_changed=False, messages=messages)

    def add_tiles(self, game: Game, country: Country, prompt: Prompt, tiles: str | list[str]) -> RollResponse:
        return self._check_cooldown(game, country, prompt,
                                    lambda: self._base.add_tiles(game, country, prompt, tiles))

    def add_expansion(self, game: Game, country: Country, prompt: Prompt) -> RollResponse:
        return self._check_cooldown(game, country, prompt,
                                    lambda: self._base.add_expansion(game, country, prompt))

    def add_against(self, game: Game, country: Country, prompt: Prompt, target: Country) -> RollResponse:
        return self._check_cooldown(game, country, prompt,
                                    lambda: self._base.add_against(game, country, prompt, target))

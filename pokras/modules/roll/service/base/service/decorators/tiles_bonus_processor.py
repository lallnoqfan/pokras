from modules.roll.responses import RollResponses
from modules.roll.service.base.models.api_things import RollPrompt
from modules.roll.service.base.models.gamestate_things import GameState, CountryState
from modules.roll.service.base.service.abc.bonus_processor import BonusProcessor


class TilesBonusProcessor(BonusProcessor):
    def process_bonus(self, game: GameState, country: CountryState, prompt: RollPrompt) -> tuple[int, str]:
        country_tiles = self.repository.get_country_tiles(country)
        bonus = sum(self.tiler.get_tile_bonus(tile.code) for tile in country_tiles)

        if bonus > 0:
            roll_value = prompt.roll_value or 0
            total_value = roll_value + bonus
            response = RollResponses.bonus(roll_value, bonus, total_value)
        else:
            response = ""

        return bonus, response

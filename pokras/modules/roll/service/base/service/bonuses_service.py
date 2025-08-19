from modules.country.models.country import Country
from modules.game.models.game import Game
from modules.roll.responses import RollResponses
from modules.roll.service.base.service.base_service import BaseService
from modules.roll.service.base.tiler.bonuses_tiler import BonusesTiler


class BonusesService(BaseService):
    """
    Простой класс, считающий сумму бонусов всех территорий игрока и добавляющий их к роллу (с ролл валью > 0)
    """
    @classmethod
    def _process_roll(cls, game: Game, country: Country, roll: list[int], response: list[str]) -> int:
        if not issubclass(cls.tiler, BonusesTiler):
            raise ValueError(f"tiler must be BonusesTiler, got {cls.tiler.__class__.__name__}")

        roll_values = cls.repository.get_roll_values(game)
        roll_value = cls.parser.get_roll_value(roll, roll_values)
        if roll_value > 0:
            bonus = sum(cls.tiler.get_tile_bonus(tile.code) for tile in country.tiles)
        else:
            bonus = 0

        total_value = roll_value + bonus
        if bonus > 0:
            response.append(RollResponses.roll_with_bonus(roll, roll_value, bonus, total_value))
        else:
            response.append(RollResponses.roll(roll, roll_value))

        return total_value

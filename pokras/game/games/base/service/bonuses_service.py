from game.games.base.service.base_service import BaseService
from game.games.base.tiler.bonuses_tiler import BonusesTiler
from game.responses.roll import RollResponses
from game.tables import Game, Country


class BonusesService(BaseService):
    """
    Простой класс, считающий сумму бонусов всех территорий игрока и добавляющий их к роллу (с ролл валью > 0)
    """
    @classmethod
    def _process_roll(cls, game: Game, country: Country, roll: list[int], response: list[str]) -> int:
        if not issubclass(cls.tiler, BonusesTiler):
            raise ValueError(f"tiler must be BonusesTiler, got {cls.tiler.__class__.__name__}")

        roll_value = cls.parser.get_roll_value(roll)
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

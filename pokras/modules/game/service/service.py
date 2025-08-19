from re import split

from modules.game.models.game import Game
from modules.game.queries.update_game import update_roll_values
from modules.game.service.models.roll_values import RollValues


def parse_values(values: str) -> RollValues | None:
    values = split(r"[,|]", values)

    try:
        values = list(map(int, values))
    except ValueError:
        return

    try:
        values = RollValues.from_list(values)
    except ValueError:
        return

    return values


def get_roll_values(game: Game) -> RollValues:
    values = game.roll_values
    values = split(r"[,|]", values)
    values = list(map(int, values))
    values = RollValues.from_list(values)
    return values


def set_roll_values(game: Game, values: RollValues) -> None:
    update_roll_values(game.id, values.dump_to_string())

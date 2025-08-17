from typing import Type

from game.games.base.service.service import Service
from game.games.eu_classic.service import EuClassicService
from game.games.korea.service import KoreaService
from game.games.ops_ass.service import OpsAssService
from game.games.stalker.service import StalkerService
from game.tables.choices.game_map import GameMap


class ServiceStrategy:
    """
    Стратегия выбора сервиса по типу карты
    """
    def __new__(cls, game_map: GameMap) -> Type[Service]:
        match game_map:
            case GameMap.eu_classic:
                return EuClassicService
            case GameMap.stalker:
                return StalkerService
            case GameMap.korea:
                return KoreaService
            case GameMap.ops_ass:
                return OpsAssService
            case _:
                raise ValueError(f"Unknown game map: {game_map}")

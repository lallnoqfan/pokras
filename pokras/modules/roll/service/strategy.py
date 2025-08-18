from typing import Type

from modules.game.models.choices.game_map import GameMap
from modules.roll.service.base.service.service import Service
from modules.roll.service.eu_classic.service import EuClassicService
from modules.roll.service.korea.service import KoreaService
from modules.roll.service.ops_ass.service import OpsAssService
from modules.roll.service.stalker.service import StalkerService


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

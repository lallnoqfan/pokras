from typing import Type

from modules.game.models.choices.game_map import GameMap
from modules.game.models.game import Game
from modules.roll.service.base.service.cooldown_service import CooldownService
from modules.roll.service.base.service.service import Service
from modules.roll.service.eu_classic.service import EuClassicService
from modules.roll.service.korea.service import KoreaService
from modules.roll.service.ops_ass.service import OpsAssService
from modules.roll.service.stalker.service import StalkerService


class ServiceStrategy:
    """
    Стратегия выбора сервиса по типу карты
    """
    def __new__(cls, game: Game) -> Type[Service]:
        match game.map:
            case GameMap.eu_classic:
                service = EuClassicService
            case GameMap.stalker:
                service = StalkerService
            case GameMap.korea:
                service = KoreaService
            case GameMap.ops_ass:
                service = OpsAssService
            case _:
                raise ValueError(f"Unknown game map: {game.map}")
        if game.use_cooldown:
            service = CooldownService(service())
        return service

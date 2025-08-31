from typing import Type

from modules.game.models.choices.game_map import GameMap
from modules.game.models.game import Game
from modules.roll.service.base.models.config import ServiceConfig
from modules.roll.service.base.painter.base_painter import BasePainter
from modules.roll.service.base.painter.layered_painter import LayeredPainter
from modules.roll.service.base.painter.painter import Painter
from modules.roll.service.base.parser.aliases_parser import AliasesParser
from modules.roll.service.base.parser.base_parser import BaseParser
from modules.roll.service.base.parser.parser import Parser
from modules.roll.service.base.repository.repository import Repository
from modules.roll.service.base.service.decorators.cooler import Cooler
from modules.roll.service.base.service.abc.service import Service
from modules.roll.service.base.service.decorators.roll_processor import HardRollProcessor
from modules.roll.service.base.service.decorators.tiles_bonus_processor import TilesBonusProcessor
from modules.roll.service.base.service.decorators.tiles_spawner import TilesRestrictedSpawner, TilesSpawner
from modules.roll.service.base.service.decorators.tiles_validator import TilesValidator
from modules.roll.service.base.service.services.live_tiles_service import LiveTilesService
from modules.roll.service.base.tiler.abc.tiler import Tiler
from modules.roll.service.base.tiler.decorators.aliases_tiler import AliasesTiler
from modules.roll.service.base.tiler.decorators.spawn_prohibited_tiler import SpawnProhibitedTiler
from modules.roll.service.base.tiler.decorators.tiles_bonuses_tiler import TilesBonusesTiler
from modules.roll.service.eu_classic.config import EuClassicConfig
from modules.roll.service.korea.config import KoreaConfig
from modules.roll.service.ops_ass.config import OpsAssConfig
from modules.roll.service.stalker.config import StalkerConfig


class ServiceFactory:
    """
    Фабрика сервиса по типу карты и параметрам игры
    """
    @classmethod
    def get_service_config(cls, game: Game) -> Type[ServiceConfig]:
        match game.map:
            case GameMap.eu_classic:
                config = EuClassicConfig
            case GameMap.stalker:
                config = StalkerConfig
            case GameMap.korea:
                config = KoreaConfig
            case GameMap.ops_ass:
                config = OpsAssConfig
            case _:
                raise ValueError(f"Unknown game map: {game.map}")

        return config

    @classmethod
    def build_service(cls, game: Game) -> Service:
        config = cls.get_service_config(game)

        tiler = cls.build_tiler(game, config)
        parser = cls.build_parser(game, config)
        painter = cls.build_painter(game, config)
        repository = cls.build_repository(game, config)

        # 1. Базовый сервис
        #    сейчас не так много опций, так что просто выбираем базовый сервис
        #    как будут регионы и пошаговые сервисы, будем брать базу из бд
        service = LiveTilesService(tiler, painter, repository, parser)

        # 2. оборачиваем базу в сервисы из конфига карты (?)
        #    тбх я пока не знаю как *лучше* организовать кастомные сервисы для карт
        service = service

        # 3. Обработка спавна
        #    сюда выносим всю логику, регулирующую спавн новых (респавн старых?) стран
        if config.use_spawn_prohibited_tiles:
            service = TilesRestrictedSpawner(service)
        else:
            service = TilesSpawner(service)

        # 4. Обработка ролла
        #    если у нас простая классика - навешиваем только базовый парсинг
        #    если есть бонусы тайлов - добавляем их
        #    как будут регионы, добавим ещё их бонусы
        bonuses_processors = []
        if config.use_tiles_bonuses:
            bonuses_processors.append(TilesBonusProcessor(service))
        service = HardRollProcessor(service, bonuses_processors)

        # 5. Превалидация
        #    отсеиваем несуществующие страны, несуществующие тайлы, етц
        validator = TilesValidator(service)
        if game.use_cooldown:
            service = Cooler(service, validator)
        else:
            service = validator

        # ?????
        # вы великолепны!
        return service

    @classmethod
    def build_painter(cls, game: Game, service_config: Type[ServiceConfig]) -> Painter:
        painter_config = service_config.painter_config
        base_painter = painter_config.base_painter

        if issubclass(base_painter, LayeredPainter):
            painter = base_painter(
                font_path=painter_config.font_path,
                map_layer=painter_config.map_layer,
                bg_layers=painter_config.bg_layers,
                fg_layers=painter_config.fg_layers,
            )

        elif issubclass(base_painter, BasePainter):
            painter = base_painter(
                font_path=painter_config.font_path,
                map_layer=painter_config.map_layer,
            )

        else:
            raise ValueError(f"Unknown painter type: {base_painter}")

        return painter

    @classmethod
    def build_parser(cls, game: Game, service_config: Type[ServiceConfig]) -> Parser:
        if service_config.use_tiles_aliases:
            parser = AliasesParser()
        else:
            parser = BaseParser()
        return parser

    @classmethod
    def build_repository(cls, game: Game, service_config: Type[ServiceConfig]) -> Repository:
        return Repository()

    @classmethod
    def build_tiler(cls, game: Game, service_config: Type[ServiceConfig]) -> Tiler:
        tiler_config = service_config.tiler_config
        tiler = tiler_config.base_tiler(tiler_config.data_path)

        if service_config.use_tiles_bonuses:
            tiler = TilesBonusesTiler(tiler)

        if service_config.use_spawn_prohibited_tiles:
            tiler = SpawnProhibitedTiler(tiler)

        if service_config.use_tiles_aliases:
            tiler = AliasesTiler(tiler)

        return tiler

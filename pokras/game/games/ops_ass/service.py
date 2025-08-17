from game.games.base.parser.aliases_parser import AliasesParser
from game.games.base.repository.base_repository import BaseRepository
from game.games.base.service.bonuses_service import BonusesService
from game.games.base.service.spawn_prohibited_service import SpawnProhibitedService
from game.games.ops_ass.painter import OpsAssPainter
from game.games.ops_ass.tiler import OpsAssTiler


class OpsAssService(SpawnProhibitedService, BonusesService):
    tiler = OpsAssTiler
    painter = OpsAssPainter
    repository = BaseRepository
    parser = AliasesParser

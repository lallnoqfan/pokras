from modules.roll.service.base.parser.aliases_parser import AliasesParser
from modules.roll.service.base.repository.base_repository import BaseRepository
from modules.roll.service.base.service.bonuses_service import BonusesService
from modules.roll.service.base.service.spawn_prohibited_service import SpawnProhibitedService
from modules.roll.service.ops_ass.painter import OpsAssPainter
from modules.roll.service.ops_ass.tiler import OpsAssTiler


class OpsAssService(SpawnProhibitedService, BonusesService):
    tiler = OpsAssTiler
    painter = OpsAssPainter
    repository = BaseRepository
    parser = AliasesParser

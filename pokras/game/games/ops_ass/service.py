from game.games.base.parser.aliases_parser import AliasesParser
from game.games.base.repository.base_repository import BaseRepository
from game.games.base.service.base_service import BaseService
from game.games.ops_ass.painter import OpsAssPainter
from game.games.ops_ass.tiler import OpsAssTiler


class OpsAssService(BaseService):
    tiler = OpsAssTiler
    painter = OpsAssPainter
    repository = BaseRepository
    parser = AliasesParser

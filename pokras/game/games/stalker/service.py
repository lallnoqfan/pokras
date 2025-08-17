from game.games.base.parser.base_parser import BaseParser
from game.games.base.repository.base_repository import BaseRepository
from game.games.base.service.base_service import BaseService
from game.games.stalker.painter import StalkerPainter
from game.games.stalker.tiler import StalkerTiler


class StalkerService(BaseService):
    tiler = StalkerTiler
    painter = StalkerPainter
    repository = BaseRepository
    parser = BaseParser

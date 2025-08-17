from game.games.base.parser.base_parser import BaseParser
from game.games.base.repository.base_repository import BaseRepository
from game.games.base.service.base_service import BaseService
from game.games.eu_classic.painter import EuClassicPainter
from game.games.eu_classic.tiler import EuClassicTiler


class EuClassicService(BaseService):
    tiler = EuClassicTiler
    painter = EuClassicPainter
    repository = BaseRepository
    parser = BaseParser

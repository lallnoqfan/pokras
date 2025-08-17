from game.games.base.parser.base_parser import BaseParser
from game.games.base.repository.base_repository import BaseRepository
from game.games.base.service.base_service import BaseService
from game.games.korea.painter import KoreaPainter
from game.games.korea.tiler import KoreaTiler


class KoreaService(BaseService):
    tiler = KoreaTiler
    painter = KoreaPainter
    repository = BaseRepository
    parser = BaseParser

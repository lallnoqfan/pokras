from modules.roll.service.base.parser.base_parser import BaseParser
from modules.roll.service.base.repository.base_repository import BaseRepository
from modules.roll.service.base.service.base_service import BaseService
from modules.roll.service.korea.painter import KoreaPainter
from modules.roll.service.korea.tiler import KoreaTiler


class KoreaService(BaseService):
    tiler = KoreaTiler
    painter = KoreaPainter
    repository = BaseRepository
    parser = BaseParser

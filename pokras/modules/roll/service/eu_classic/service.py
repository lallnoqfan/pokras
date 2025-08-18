from modules.roll.service.base.parser.base_parser import BaseParser
from modules.roll.service.base.repository.base_repository import BaseRepository
from modules.roll.service.base.service.base_service import BaseService
from modules.roll.service.eu_classic.painter import EuClassicPainter
from modules.roll.service.eu_classic.tiler import EuClassicTiler


class EuClassicService(BaseService):
    tiler = EuClassicTiler
    painter = EuClassicPainter
    repository = BaseRepository
    parser = BaseParser

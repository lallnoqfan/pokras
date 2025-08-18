from modules.roll.service.base.parser.base_parser import BaseParser
from modules.roll.service.base.repository.base_repository import BaseRepository
from modules.roll.service.base.service.base_service import BaseService
from modules.roll.service.stalker.painter import StalkerPainter
from modules.roll.service.stalker.tiler import StalkerTiler


class StalkerService(BaseService):
    tiler = StalkerTiler
    painter = StalkerPainter
    repository = BaseRepository
    parser = BaseParser

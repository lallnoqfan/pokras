from config import Paths
from modules.roll.service.base.tiler.aliases_tiler import AliasesTiler
from modules.roll.service.base.tiler.bonuses_tiler import BonusesTiler
from modules.roll.service.base.tiler.spawn_prohibited_tiler import SpawnProhibitedTiler


class OpsAssTiler(AliasesTiler, SpawnProhibitedTiler, BonusesTiler):
    DATA_PATH = Paths.OPS_ASS_TILES

from config import Paths
from game.games.base.tiler.aliases_tiler import AliasesTiler
from game.games.base.tiler.bonuses_tiler import BonusesTiler
from game.games.base.tiler.spawn_prohibited_tiler import SpawnProhibitedTiler


class OpsAssTiler(AliasesTiler, SpawnProhibitedTiler, BonusesTiler):
    DATA_PATH = Paths.OPS_ASS_TILES

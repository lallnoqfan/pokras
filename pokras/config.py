from os import getenv
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".env"))


def _getenv_bool(key: str, default_value: bool = False) -> bool:
    return getenv(key, str(default_value)).lower() in ("1", "true")


class AppConfig:
    VERBOSE_DB = _getenv_bool("VERBOSE_DB")
    VERBOSE_PERFORMANCE = _getenv_bool("VERBOSE_PERFORMANCE")


class BotConfig:
    APP_ID = getenv("APP_ID")
    BOT_TOKEN = getenv("BOT_TOKEN")
    PUBLIC_KEY = getenv("PUBLIC_KEY")


class ConnectionConfig:
    USE_PROXY = _getenv_bool("USE_PROXY")
    PROXY_URL = getenv("PROXY_URL", None) if USE_PROXY else None


class Paths:
    BASE = Path(__file__).parent.parent.resolve()
    PROJECT_ROOT = BASE / "pokras"
    SQLITE_DB = BASE / "db.sqlite"

    RESOURCES = BASE / "resources"
    MAPS = RESOURCES / "maps"
    FONTS = RESOURCES / "fonts"

    EU_CLASSIC = MAPS / "eu_classic"
    EU_CLASSIC_MAP = EU_CLASSIC / "map.png"
    EU_CLASSIC_TILES = EU_CLASSIC / "tiles_data.json"

    STALKER = MAPS / "stalker"
    STALKER_MAP = STALKER / "map.png"
    STALKER_TILES = STALKER / "tiles_data.json"

    KOREA = MAPS / "korea"
    KOREA_MAP = KOREA / "map.png"
    KOREA_TILES = KOREA / "tiles_data.json"

    OPS_ASS = MAPS / "ops_ass"
    OPS_ASS_MAP = OPS_ASS / "map.png"
    OPS_ASS_TILES = OPS_ASS / "tiles_data.json"

    SRADTARCTICA = MAPS / "sradtarctica"

    FONT_CODENAME = FONTS / "CodenameCoderFree4F-Bold.ttf"

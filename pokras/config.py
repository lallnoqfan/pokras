from os import getenv
from pathlib import Path

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv(".env"))


def _getenv_bool(key: str, default_value: bool = False) -> bool:
    return getenv(key, str(default_value)).lower() in ("1", "true")


class BotConfig:
    APP_ID = getenv("APP_ID")
    BOT_TOKEN = getenv("BOT_TOKEN")
    PUBLIC_KEY = getenv("PUBLIC_KEY")


class ConnectionConfig:
    USE_PROXY = _getenv_bool("USE_PROXY")
    PROXY_URL = getenv("PROXY_URL", None) if USE_PROXY else None


class Paths:
    BASE = getenv("BASE_PATH", Path(__file__).parent.parent)
    RESOURCES = BASE / "resources"

    MAP = RESOURCES / "map.png"
    TILES_DATA = RESOURCES / "tiles_data.json"
    RULES = RESOURCES / "rules.txt"
    FONT = RESOURCES / "CodenameCoderFree4F-Bold.ttf"


class AppConfig:
    DEBUG = _getenv_bool("DEBUG")

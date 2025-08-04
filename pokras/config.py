from os import getenv

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

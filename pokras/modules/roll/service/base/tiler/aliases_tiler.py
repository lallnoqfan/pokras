from abc import ABC

from modules.roll.service.base.tiler.base_tiler import BaseTiler


class AliasesTiler(BaseTiler, ABC):
    @classmethod
    def get_alias(cls, alias: str) -> str:
        aliases = cls._load_data().get("tiles_aliases", {})
        return aliases.get(alias, alias)

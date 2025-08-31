from modules.roll.service.base.tiler.abc.tiler_decorator import TilerDecorator


class AliasesTiler(TilerDecorator):
    def get_by_alias(self, alias: str) -> str:
        aliases = self._load_data().tiles_aliases
        return aliases.get(alias, alias)

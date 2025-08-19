from abc import ABC, abstractmethod

from modules.country.models.country import Country
from modules.game.models.game import Game
from modules.game.service.models.roll_values import RollValues


class Repository(ABC):
    """
    Абстрактный класс, отвечающий за чтение состояния игры.
    Прячет внутри себя доступ к бд / другому хранилищу состояния.
    """
    @classmethod
    @abstractmethod
    def get_tile_owner(cls, game: Game, tile_code: str) -> Country | None:
        ...

    @classmethod
    @abstractmethod
    def set_tile_owner(cls, game: Game, country: Country, tile_code: str) -> None:
        ...

    @classmethod
    @abstractmethod
    def get_roll_values(cls, game: Game) -> RollValues:
        ...

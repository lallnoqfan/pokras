from abc import ABC, abstractmethod

from game.tables import Game, Country


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

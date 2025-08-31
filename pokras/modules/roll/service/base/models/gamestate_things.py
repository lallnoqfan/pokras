from dataclasses import dataclass
from datetime import timedelta, datetime

from modules.game.models.choices.game_map import GameMap


@dataclass
class LastRollState:
    """
    Маппинг игра - юзер - таймстемп последнего ролла от юзера в игре.
    """
    id: int
    user_id: int
    game_id: int
    timestamp: datetime


@dataclass
class TileState:
    """
    Моделька тайла.

    Attributes:
        id: айди тайла
        code: код тайла
        game_id: айди игры
        owner_id: айди страны, владеющей тайлом
    """
    id: int
    code: str
    game_id: int
    owner_id: int | None


@dataclass
class CountryState:
    """
    Моделька страны.

    Attributes:
        id: айди страны
        name: название страны (50 символов)
        color: hex-цвет страны (7 символов)
        game_id: айди игры
        creator_id: айди игрока, создавшего страну
    """
    id: int
    name: str
    color: str
    game_id: int
    creator_id: int


@dataclass
class GameState:
    """
    Моделька игры.

    Attributes:
        id: айди игры
        channel: айди канала
        is_active: активна ли игра
        map: карта
        roll_values: строка значений роллов
        use_cooldown: используется ли в игре кулдаун
        cooldown: время кулдауна
    """
    id: int
    channel: int
    is_active: bool
    map: GameMap
    roll_values: str
    use_cooldown: bool
    cooldown: timedelta | None

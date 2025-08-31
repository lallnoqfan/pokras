from dataclasses import dataclass
from datetime import datetime


@dataclass
class RollResponse:
    """
    Attributes:
        ok: был ли ролл валидным
        map_state_changed: изменилось ли состояние карты после применения ролла
        messages: список сообщений, которые будут отправлены пользователю
    """
    ok: bool
    map_state_changed: bool
    messages: list[str]


@dataclass
class RollPrompt:
    country: str
    roll: list[int]
    timestamp: datetime
    roll_value: int | None


@dataclass
class TilesRollPrompt(RollPrompt):
    tiles: list[str]


@dataclass
class ExpansionRollPrompt(RollPrompt):
    ...


@dataclass
class AgainstRollPrompt(RollPrompt):
    target: str

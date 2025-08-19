from dataclasses import dataclass


@dataclass
class RollResponse:
    ok: bool
    map_state_changed: bool
    messages: list[str]

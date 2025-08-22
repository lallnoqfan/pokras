from datetime import timedelta

from db.engine import session
from modules.game.models.choices.game_map import GameMap
from modules.game.models.game import Game


def create_game(channel_id: int, game_map: GameMap, dumped_roll_values: str,
                use_cooldown: bool, cooldown: timedelta) -> Game:
    new_game = Game(
        channel=channel_id, is_active=True, map=game_map, roll_values=dumped_roll_values,
        use_cooldown=use_cooldown, cooldown=cooldown,
    )
    session.add(new_game)
    session.commit()
    session.refresh(new_game)
    return new_game

from db.engine import session
from modules.game.models.choices.game_map import GameMap
from modules.game.models.game import Game


def create_game(channel_id: int, game_map: GameMap) -> Game:
    new_game = Game(channel=channel_id, is_active=True, map=game_map)
    session.add(new_game)
    session.commit()
    session.refresh(new_game)
    return new_game

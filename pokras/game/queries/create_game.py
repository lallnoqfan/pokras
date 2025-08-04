from db.engine import session
from game.tables import Game


def create_game(channel_id: int) -> Game:
    new_game = Game(channel=channel_id, is_active=True)
    session.add(new_game)
    session.commit()
    session.refresh(new_game)
    return new_game

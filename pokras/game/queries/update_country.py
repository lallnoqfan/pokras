from sqlalchemy import update

from db.engine import session
from game.tables import Game, Country


def set_country_name(game_id: int, country_id: int, new_name: str) -> None:
    stmt = (update(Country)
            .where(Game.id == game_id, Country.id == country_id)
            .values(name=new_name))
    session.execute(stmt)
    session.commit()


def set_country_color(game_id: int, country_id: int, new_color: str) -> None:
    stmt = (update(Country)
            .where(Game.id == game_id, Country.id == country_id)
            .values(color=new_color))
    session.execute(stmt)
    session.commit()

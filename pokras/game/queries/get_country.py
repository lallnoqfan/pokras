from sqlalchemy import select

from db.engine import session
from game.tables import Country, Game


def get_country_by_color(game_id: int, color: str) -> Country | None:
    stmt = select(Country).where(Game.id == game_id, Country.color == color)
    return session.scalars(stmt).first()


def get_country_by_name(game_id: int, name: str) -> Country | None:
    stmt = select(Country).where(Game.id == game_id, Country.name == name)
    return session.scalars(stmt).first()

from sqlalchemy import select

from db.engine import session
from modules.country.models.country import Country


def get_country(country_id: int) -> Country | None:
    stmt = select(Country).where(Country.id == country_id)
    return session.scalars(stmt).first()


def get_country_by_color(game_id: int, color: str) -> Country | None:
    stmt = select(Country).where(Country.game_id == game_id, Country.color == color)
    return session.scalars(stmt).first()


def get_country_by_name(game_id: int, name: str) -> Country | None:
    stmt = select(Country).where(Country.game_id == game_id, Country.name == name)
    return session.scalars(stmt).first()


def get_countries_by_game_id(game_id: int) -> list[Country]:
    stmt = select(Country).where(Country.game_id == game_id)
    return session.scalars(stmt).all()

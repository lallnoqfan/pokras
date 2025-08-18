from db.engine import session
from modules.country.models.country import Country


def create_country(name: str, color: str, game_id: int, creator_id: int) -> Country:
    new_country = Country(name=name, color=color, game_id=game_id, creator_id=creator_id)
    session.add(new_country)
    session.commit()
    session.refresh(new_country)
    return new_country

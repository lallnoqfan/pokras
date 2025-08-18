from dataclasses import dataclass, field


@dataclass
class CountryModel:
    """
    Моделька страны, используемая для рендера карты и легенды.

    Attributes:
        name: Название страны
        hex_color: Цвет страны в HEX формате
        tiles: Список кодов тайлов, которые принадлежат данной стране
    """
    name: str
    hex_color: str
    tiles: list[str] = field(default_factory=lambda: [])

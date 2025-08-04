from game.text.tags import Tags as T


class Responses:
    @staticmethod
    def country_added(player_name: str) -> str:
        return f"добавлена страна {player_name}\n"

    @staticmethod
    def country_created(tile: str, player_name: str) -> str:
        return T.bold(f"\"{player_name}\" создаётся на {tile.upper()}")

    @staticmethod
    def creation_attack(tile: str, player_name: str, attacked_name: str) -> str:
        return T.bold(f"\"{player_name}\" создаётся на {tile.upper()}, захватывая клетку \"{attacked_name}\"")

    @staticmethod
    def capture(tile: str, player_name: str) -> str:
        return f"\"{player_name}\" захватывает нейтральную {tile.upper()}"

    @staticmethod
    def capture_attack(tile: str, player_name: str, attacked_name: str) -> str:
        return T.bold(f"\"{player_name}\" захватывает {tile.upper()} у \"{attacked_name}\"")

    @staticmethod
    def same_name(player_name: str) -> str:
        return T.spoiler(f"имя \"{player_name}\" занято")

    @staticmethod
    def same_color(color_code: str) -> str:
        return T.spoiler(f"цвет #{color_code} занят")

    @staticmethod
    def too_long_name() -> str:
        # hopefully one day... # todo: fix hardcode
        return T.spoiler("макс. длина названия - 50 символов")

    @staticmethod
    def non_cyrillic_name() -> str:
        return T.spoiler("имя может содержать только кириллицу и пробелы")

    @staticmethod
    def creation_denied(reason: str | None) -> str:
        return T.spoiler(f"создание запрещено" + (f", причина: {reason}" if reason else ""))

    @classmethod
    def black_listed_name(cls) -> str:
        return cls.creation_denied("имя в черном списке")

    @staticmethod
    def already_owns(tile: str) -> str:
        return T.spoiler(f"{tile.upper()} уже под вашим контролем")

    @staticmethod
    def no_routes(tile: str) -> str:
        return T.spoiler(f"нет доступных путей к {tile.upper()}")

    @staticmethod
    def invalid_tile(tile: str) -> str:
        return T.spoiler(f"территория {tile.upper()} не существует")

    @staticmethod
    def expansion_without_tiles() -> str:
        return T.spoiler("нельзя роллить на расширение, если у вас нет территорий")

    @staticmethod
    def expansion_no_free_tiles() -> str:
        return T.spoiler("нет доступных для расширения территорий")

    @staticmethod
    def against_without_tiles() -> str:
        return T.spoiler("нельзя роллить на атаку, если у вас нет территорий")

    @staticmethod
    def against_no_tiles(attacked_name: str) -> str:
        return T.spoiler(f"{attacked_name} не имеет территорий")

    @staticmethod
    def against_no_routes(attacked_name: str) -> str:
        return T.spoiler(f"нет доступных путей к \"{attacked_name}\"")

    @staticmethod
    def against_no_matches(attacked_name: str) -> str:
        return T.spoiler(f"не найдено стран с указанным именем: {attacked_name}")

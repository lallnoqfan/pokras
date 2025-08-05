from game.tables import Country
from game.utils.tags import Tags as T


class CountryResponses:

    # ========= MISSING ARGUMENTS =========

    @staticmethod
    def missing_name() -> str:
        return T.spoiler("country name is required")

    @staticmethod
    def missing_new_name() -> str:
        return T.spoiler("new country name is required")

    @staticmethod
    def missing_color() -> str:
        return T.spoiler("country color is required")

    @staticmethod
    def missing_new_color() -> str:
        return T.spoiler("new country color is required")

    # ========= FAILURE =========

    @staticmethod
    def too_long_name() -> str:
        # hopefully one day... # todo: fix hardcode
        # todo: check the name length before country creation
        #       if it's too long, notify user
        return T.spoiler("max. length for country name is 50 symbols")

    @staticmethod
    def country_not_found(country_name: str) -> str:
        return T.spoiler(f"country \"{country_name}\" not found")

    @staticmethod
    def color_already_exists(country: Country) -> str:
        return T.spoiler(f"country with this color already exists: {country}")

    @staticmethod
    def name_already_exists(country: Country) -> str:
        return T.spoiler(f"country with this name already exists: {country}")

    @staticmethod
    def new_name_already_exists(country: Country) -> str:
        return T.spoiler(f"country with this new name already exists: {country}")

    @staticmethod
    def not_creator(country: Country) -> str:
        return T.spoiler(f"you are not the creator of this country: {country}")

    # ========= SUCCESS =========

    @staticmethod
    def list_countries(countries: list[Country]) -> str:
        if not countries:
            return "no countries found"

        response = "countries:\n"
        for country in countries:
            response += f"- {country}\n"
        return response

    @staticmethod
    def country_created(country: Country) -> str:
        return f"country created: {country}"

    @staticmethod
    def name_changed(country: Country) -> str:
        return f"country renamed: {country}"

    @staticmethod
    def color_changed(country: Country) -> str:
        return f"country color changed: {country}"

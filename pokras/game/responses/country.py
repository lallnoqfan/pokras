from game.tables import Country


class CountryResponses:

    # ========= MISSING ARGUMENTS =========

    @staticmethod
    def missing_name() -> str:
        return "country name is required"

    @staticmethod
    def missing_new_name() -> str:
        return "new country name is required"

    @staticmethod
    def missing_color() -> str:
        return "country color is required"

    @staticmethod
    def missing_new_color() -> str:
        return "new country color is required"

    # ========= FAILURE =========

    @staticmethod
    def country_not_found() -> str:
        return "country not found"

    @staticmethod
    def color_already_exists(country: Country) -> str:
        return f"country with this color already exists: {country}"

    @staticmethod
    def name_already_exists(country: Country) -> str:
        return f"country with this name already exists: {country}"

    @staticmethod
    def new_name_already_exists(country: Country) -> str:
        return f"country with this new name already exists: {country}"

    @staticmethod
    def not_creator(country: Country) -> str:
        return f"you are not the creator of this country: {country}"

    # ========= SUCCESS =========

    @staticmethod
    def country_created(country: Country) -> str:
        return f"country created: {country}"

    @staticmethod
    def name_changed(country: Country) -> str:
        return f"country renamed: {country}"

    @staticmethod
    def color_changed(country: Country) -> str:
        return f"country color changed: {country}"

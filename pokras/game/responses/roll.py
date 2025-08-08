from game.utils.tags import Tags as T


class RollResponses:

    # ========= MISSING ARGUMENTS =========

    @staticmethod
    def missing_prompt() -> str:
        return T.spoiler("prompt is required")

    # ========= FAILURE =========

    @staticmethod
    def invalid_tile(tile: str) -> str:
        return T.spoiler(f"{tile.upper()} is not a valid tile")

    @staticmethod
    def expansion_without_tiles() -> str:
        return T.spoiler("you cannot roll on expansion if you don't control any tiles")

    @staticmethod
    def against_without_tiles() -> str:
        # todo: on against roll, check if country has tiles
        #       if not, notify user
        return T.spoiler("you cannot roll against someone if you don't control any tiles")

    @staticmethod
    def expansion_no_free_tiles() -> str:
        return T.spoiler("there is no available free tile to roll on expansion")

    @staticmethod
    def against_no_tiles(attacked_name: str) -> str:
        # todo: on against roll, check if attacked country has any tiles
        #       if not, notify user
        return T.spoiler(f"{attacked_name} doesn't control any tiles")

    @staticmethod
    def capture_no_route(tile: str) -> str:
        #     : on tile roll, check if there is direct access to the tile
        #       also, there might be direct access to previously unreachable tile after capture,
        #       so notify user only if some tiles might be wasted
        return T.spoiler(f"there is no direct access from your tiles to {tile.upper()}")

    @staticmethod
    def against_no_routes(attacked_name: str) -> str:
        # todo: on against roll, check if there is any direct access to attacked country's tiles
        #       if not, notify user
        return T.spoiler(f"there is no route from your tiles to \"{attacked_name}\"'s")

    @staticmethod
    def capture_owned(tile: str) -> str:
        return T.spoiler(f"you already control {tile.upper()}")

    @staticmethod
    def roll_value_surplus(surplus: int) -> str:
        end = 'а' if surplus == 1 else 'ов'
        return T.spoiler(f"излишек из {surplus} захват{end} не был распределён и сгорает")

    # ========= SUCCESS =========

    @staticmethod
    def roll(nums: list[int], roll_value: int) -> str:
        response = " ".join(map(lambda n: T.code(str(n)), nums))
        response += f" = {roll_value} tile{'s' if roll_value != 1 else ''}"
        return response

    @staticmethod
    def spawn(country_name: str, tile_id: str) -> str:
        return T.bold(f"\"{country_name}\" spawned at {tile_id.upper()}")

    @staticmethod
    def spawn_attack(country_name: str, tile_id: str, attacked_name: str) -> str:
        return T.bold(f"\"{country_name}\" captured \"{attacked_name}\"'s tile and spawned at {tile_id.upper()}")

    @staticmethod
    def capture_neutral(country_name: str, tile_id: str) -> str:
        return f"\"{country_name}\" captured {tile_id.upper()}"

    @staticmethod
    def capture_attack(country_name: str, tile_id: str, attacked_name: str) -> str:
        return T.bold(f"\"{country_name}\" captured \"{attacked_name}\"'s {tile_id.upper()}")

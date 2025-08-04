from game.tables import Game


class GameResponses:

    # ========= MISSING ARGUMENTS =========

    @staticmethod
    def missing_game_id() -> str:
        return "game id is required"

    # ========= FAILURE =========

    @staticmethod
    def game_not_found() -> str:
        return "game not found"

    @staticmethod
    def active_game_already_exists(game: Game) -> str:
        return f"an active game for this channel already exists: {game}"

    @staticmethod
    def no_active_games() -> str:
        return "there is no active game for this channel"

    # ========= SUCCESS =========

    @staticmethod
    def list_games(games: list[Game]) -> str:
        if not games:
            return "no games found"

        response = "games:\n"
        for game in games:
            response += f"- {game}\n"
        return response

    @staticmethod
    def game_created(game: Game) -> str:
        return f"game created: {game}"

    @staticmethod
    def game_started(game: Game) -> str:
        return f"game started: {game}"

    @staticmethod
    def game_stopped(game: Game) -> str:
        return f"game stopped: {game}"

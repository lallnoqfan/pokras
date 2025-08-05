from discord.ext.commands import Cog, command, Context

from game.commands.checks import has_active_game, has_no_active_games, is_admin_or_dm
from game.queries.create_game import create_game
from game.queries.get_game import get_games_by_channel_id, get_active_game_by_channel_id, get_game_by_id
from game.queries.update_game import set_game_inactive, set_game_active
from game.responses.game import GameResponses


class GameCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def list_games(self, ctx: Context):
        """
        Возвращает список игр для текущего канала
        """
        channel_id = ctx.channel.id
        games = get_games_by_channel_id(channel_id)
        response = GameResponses.list_games(games)
        await ctx.send(response)

    @command()
    @is_admin_or_dm()
    @has_no_active_games()
    async def create_game(self, ctx: Context):
        """
        Создаёт новую игру в текущем канале
        """
        channel_id = ctx.channel.id
        game = create_game(channel_id)
        response = GameResponses.game_created(game)
        await ctx.send(response)

    @command()
    @is_admin_or_dm()
    @has_active_game()
    async def stop_game(self, ctx: Context):
        """
        Останавливает активную игру в текущем канале
        """
        channel_id = ctx.channel.id
        game = get_active_game_by_channel_id(channel_id)
        set_game_inactive(game.id)
        response = GameResponses.game_stopped(game)
        await ctx.send(response)

    @command()
    @is_admin_or_dm()
    @has_no_active_games()
    async def start_game(self, ctx: Context, game_id: int | None):
        """
        Возобновляет остановленную игру в текущем канале

        Args:
            game_id: id игры
        """
        if not game_id:
            response = GameResponses.missing_game_id()
            await ctx.send(response)
            return

        game = get_game_by_id(game_id)
        if not game:
            response = GameResponses.game_not_found()
            await ctx.send(response)
            return

        if game.channel != ctx.channel.id:
            response = GameResponses.wrong_channel()
            await ctx.send(response)
            return

        set_game_active(game.id)
        response = GameResponses.game_started(game)
        await ctx.send(response)

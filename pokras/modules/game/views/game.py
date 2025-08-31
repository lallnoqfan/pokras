from datetime import timedelta

from discord.ext.commands import Cog, group, guild_only, Context, CheckFailure, BadArgument

from modules.game.models.choices.game_map import GameMap
from modules.game.queries.create_game import create_game
from modules.game.queries.get_game import get_active_game_by_channel_id, get_games_by_channel_id, get_game_by_id
from modules.game.queries.update_game import set_game_inactive, set_game_active
from modules.game.responses import GameResponses
from modules.game.service.models.roll_values import RollValues
from utils.checks import has_active_game, is_admin, has_no_active_games


class GameGroup(Cog):
    @group()
    async def game(self, ctx: Context): ...

    @game.command(name="list")
    @guild_only()
    async def list_games(self, ctx: Context):
        """
        Возвращает список игр для текущего канала
        """
        channel_id = ctx.channel.id
        games = get_games_by_channel_id(channel_id)
        response = GameResponses.list_games(games)
        await ctx.send(response)

    @game.command(name="create")
    @guild_only()
    @is_admin()
    @has_no_active_games()
    async def create_game(self, ctx: Context, game_map: GameMap = GameMap.eu_classic):
        """
        Создаёт новую игру в текущем канале

        Args:
            game_map: карта, на которой будет вестись игра
        """
        # todo: let user set game args such as use_cooldown, cooldown, roll_values, etc
        # and also move all logic to service
        channel_id = ctx.channel.id
        roll_values = RollValues().dump_to_string()
        use_cooldown = False
        cooldown = timedelta(seconds=0)
        game = create_game(channel_id, game_map, roll_values, use_cooldown, cooldown)
        response = GameResponses.game_created(game)
        await ctx.send(response)

    @create_game.error
    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, CheckFailure):
            pass

        elif isinstance(error, BadArgument):
            await ctx.send(GameResponses.invalid_map())

        else:
            raise error

    @game.command(name="start")
    @guild_only()
    @is_admin()
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

    @game.command(name="stop")
    @guild_only()
    @is_admin()
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

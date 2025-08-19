from discord.ext.commands import Cog, command, guild_only, Context, CheckFailure, BadArgument, group, Converter

from modules.game.models.choices.game_map import GameMap
from modules.game.queries.create_game import create_game
from modules.game.queries.get_game import get_games_by_channel_id, get_active_game_by_channel_id, get_game_by_id
from modules.game.queries.update_game import set_game_inactive, set_game_active
from modules.game.responses import GameResponses
from modules.game.service.models.roll_type import RollType
from modules.game.service.service import parse_values, set_roll_values, get_roll_values
from utils.checks import is_admin, has_no_active_games, has_active_game


class RollTypeConverter(Converter):
    async def convert(self, ctx: Context, argument: str):
        try:
            return RollType[argument.lower()]
        except KeyError:
            for member in RollType:
                if member.value == argument:
                    return member
            raise BadArgument(f'"{argument}" is not a valid roll type.')


class GameCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @group()
    @guild_only()
    async def game(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help("game")

    @game.command()
    @has_active_game()
    async def info(self, ctx: Context):
        game = get_active_game_by_channel_id(ctx.channel.id)
        response = [f"Карта: {game.map}",]
        v = parse_values(game.roll_values)
        response.append(v.dump_to_info_message())
        response = "\n".join(response)
        await ctx.send(response)

    @game.group()
    @is_admin()
    async def set(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help("game set")

    @set.command(name="roll")
    async def set_roll(self, ctx: Context, value_type: RollTypeConverter, value: int):
        if value < 0:
            await ctx.send("fail")
            return

        game = get_active_game_by_channel_id(ctx.channel.id)
        roll_values = get_roll_values(game)
        setattr(roll_values, value_type.name, value)
        set_roll_values(game, roll_values)

        await ctx.send("ok")

    @set.command(name="rolls")
    async def set_rolls(self, ctx: Context, roll_values: str):
        values = parse_values(roll_values)
        if values is None:
            await ctx.send("fail")
            return
        game = get_active_game_by_channel_id(ctx.channel.id)
        set_roll_values(game, values)
        await ctx.send("ok")

    @command()
    @guild_only()
    async def list_games(self, ctx: Context):
        """
        Возвращает список игр для текущего канала
        """
        channel_id = ctx.channel.id
        games = get_games_by_channel_id(channel_id)
        response = GameResponses.list_games(games)
        await ctx.send(response)

    @command()
    @guild_only()
    @is_admin()
    @has_no_active_games()
    async def create_game(self, ctx: Context, game_map: GameMap = GameMap.eu_classic):
        """
        Создаёт новую игру в текущем канале

        Args:
            game_map: карта, на которой будет вестись игра
        """
        channel_id = ctx.channel.id
        game = create_game(channel_id, game_map)
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

    @command()
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

    @command()
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

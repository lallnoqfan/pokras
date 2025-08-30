from discord.ext.commands import Cog, group, Context, command

from modules.game.queries.get_game import get_active_game_by_channel_id
from modules.game.views import GameCommands
from utils.perf import time_async
from utils.text import Tags as T


class TestCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def ping(self, ctx: Context):
        """
        pong.. ?
        """
        await ctx.reply("pong")

    @group(name="test")
    async def test(self, ctx: Context):
        """
        Monkey testing
        """
        if ctx.invoked_subcommand is None:
            await ctx.send_help("test")

    @test.command(name="game")
    async def test_game(self, ctx: Context):
        game_cog = GameCommands(self.bot)
        initial_game = get_active_game_by_channel_id(ctx.channel.id)
        invoke = time_async(ctx.invoke)

        if initial_game is not None:
            await ctx.send(f"{T.code('0/5')} invoking stop_game")
            _, time = await invoke(game_cog.stop_game, ctx)
            await ctx.send(T.code(f"{round(time, 4)}s"))

        await ctx.send(f"{T.code('1/5')} invoking list_games")
        _, time = await invoke(game_cog.list_games, ctx)
        await ctx.send(T.code(f"{round(time, 4)}s"))

        await ctx.send(f"{T.code('2/5')} invoking create_game")
        _, time = await invoke(game_cog.create_game, ctx)
        await ctx.send(T.code(f"{round(time, 4)}s"))

        new_game = get_active_game_by_channel_id(ctx.channel.id)
        await ctx.send(f"{T.code('3/5')} invoking stop_game")
        _, time = await invoke(game_cog.stop_game, ctx)
        await ctx.send(T.code(f"{round(time, 4)}s"))

        await ctx.send(f"{T.code('4/5')} invoking start_game")
        _, time = await invoke(game_cog.start_game, ctx, new_game.id)
        await ctx.send(T.code(f"{round(time, 4)}s"))

        await ctx.send(f"{T.code('5/5')} invoking stop_game")
        _, time = await invoke(game_cog.stop_game, ctx)
        await ctx.send(T.code(f"{round(time, 4)}s"))

        if initial_game is not None:
            await ctx.send(f"{T.code('6/5')} invoking start_game")
            _, time = await invoke(game_cog.start_game, ctx, initial_game.id)
            await ctx.send(T.code(f"{round(time, 4)}s"))

        await ctx.send("show is over")

    @test.command(name="roll")
    async def game_tests(self, ctx: Context):
        ...

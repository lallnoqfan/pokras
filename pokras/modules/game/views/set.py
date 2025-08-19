from datetime import timedelta

from discord.ext.commands import Cog, Bot, group, Context, BadArgument

from modules.game.queries.get_game import get_active_game_by_channel_id
from modules.game.queries.update_game import remove_cooldown, set_cooldown
from modules.game.service.models.roll_type import RollType
from modules.game.service.service import get_roll_values, set_roll_values, parse_values
from modules.game.converters.roll_type import RollTypeConverter
from utils.checks import is_admin


class SetGroup(Cog):
    @group()
    async def game(self, ctx: Context): ...

    @game.group()
    @is_admin()  # todo: or gm
    async def set(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help("game set")

    @set.command(name="roll")
    async def set_roll(self, ctx: Context, value_type: RollTypeConverter, value: int):
        value_type: RollType

        if value < 0:
            await ctx.reply("fail")
            return

        game = get_active_game_by_channel_id(ctx.channel.id)
        roll_values = get_roll_values(game)
        setattr(roll_values, value_type.name, value)
        set_roll_values(game, roll_values)

        await ctx.reply("ok")

    @set.command(name="rolls")
    async def set_rolls(self, ctx: Context, roll_values: str):
        values = parse_values(roll_values)
        if values is None:
            await ctx.send("fail")
            return
        game = get_active_game_by_channel_id(ctx.channel.id)
        set_roll_values(game, values)
        await ctx.reply("ok")

    @set.command(name="cooldown")
    async def set_cooldown(self, ctx: Context, value: int):
        if value < 0:
            await ctx.reply("fail")
            return

        game = get_active_game_by_channel_id(ctx.channel.id)
        if game is None:
            await ctx.reply("fail")
            return

        if value == 0:
            remove_cooldown(game.id)
            await ctx.reply("ok")
            return

        cooldown = timedelta(seconds=value)
        set_cooldown(game.id, cooldown)
        await ctx.reply("ok")

    @set_roll.error
    @set_rolls.error
    async def set_roll_error(self, ctx: Context, error: Exception):
        if isinstance(error, BadArgument):
            await ctx.reply(f"{error}")
        else:
            await ctx.reply(f"{error}")

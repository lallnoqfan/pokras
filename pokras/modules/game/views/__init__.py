from discord.ext.commands import Cog, Bot, group, guild_only, Context

from modules.game.views.game import GameGroup
from modules.game.views.info import InfoGroup
from modules.game.views.set import SetGroup


class GameCommands(GameGroup, SetGroup, InfoGroup, Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @group()
    @guild_only()
    async def game(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help("game")

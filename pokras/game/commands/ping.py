from discord.ext.commands import Cog, command, Context


class TestCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def ping(self, ctx: Context):
        """
        pong.. ?
        """
        await ctx.reply("pong")

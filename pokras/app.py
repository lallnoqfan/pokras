from discord import Intents
from discord.ext.commands import Context, Bot, check

from commands.game import GameCommands
from config import BotConfig, ConnectionConfig


def is_admin():
    """
    A custom check decorator that verifies if the command invoker has
    administrator permissions in the guild.
    """
    async def predicate(ctx: Context):
        if ctx.author.guild_permissions.administrator:
            return True
        else:
            await ctx.send(f"Sorry, {ctx.author.mention}, you must be an administrator to use this command.")
            return False
    return check(predicate)


class App(Bot):
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("=" * 30)
        await self.add_cog(GameCommands(self))


def main() -> None:
    intents = Intents.default()
    intents.message_content = True

    app = App(
        intents=intents,
        command_prefix="!",
        proxy=ConnectionConfig.PROXY_URL,
    )

    app.run(BotConfig.BOT_TOKEN)


if __name__ == '__main__':
    main()

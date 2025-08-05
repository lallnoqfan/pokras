from discord import Intents
from discord.ext.commands import Bot

from config import BotConfig, ConnectionConfig
from game.commands.country import CountryCommands
from game.commands.game import GameCommands
from game.commands.roll import RollCommands
from game.commands.test import TestCommands


class App(Bot):
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("=" * 30)
        await self.add_cog(GameCommands(self))
        await self.add_cog(CountryCommands(self))
        await self.add_cog(RollCommands(self))
        await self.add_cog(TestCommands(self))


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

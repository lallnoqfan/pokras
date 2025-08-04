from discord import Intents, Client, Message

from config import BotConfig, ConnectionConfig


class App(Client):
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("=" * 30)

    async def on_message(self, message: Message):
        channel = message.channel
        content = message.content
        author = message.author

        if not content.startswith(f"<@{self.user.id}>"):
            return

        if author.id == self.user.id:
            return

        if channel.name != "ботодрисня":
            await channel.send(f"<@{author.id}> gtfo to <#1401925169806835734>")
            return

        if content.startswith(f"<@{self.user.id}> !hello"):
            await channel.send(f"<@{author.id}> Hello!")
            return

        if content.startswith(f"<@{self.user.id}> !ping"):
            await channel.send(f"<@{author.id}> Pong!")
            return

        if content.startswith(f"<@{self.user.id}> !help"):
            await channel.send(f"<@{author.id}> Available commands:\n!hello\n!ping")
            return

        await channel.send(f"<@{author.id}> try !help command")


def main() -> None:
    intents = Intents.default()
    intents.message_content = True

    client = App(intents=intents, proxy=ConnectionConfig.PROXY_URL)
    client.run(BotConfig.BOT_TOKEN)


if __name__ == '__main__':
    main()

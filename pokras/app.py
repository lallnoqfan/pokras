from io import BytesIO

from PIL import Image
from discord import Intents, Client, Message, File

from config import BotConfig, ConnectionConfig, DataConfig


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

        if content.startswith(f"<@{self.user.id}> !map"):
            map_image = Image.open(DataConfig.RESOURCES / "map.png")
            with BytesIO() as image_binary:
                map_image.save(image_binary, 'PNG')
                image_binary.seek(0)
                map_image = File(fp=image_binary, filename="map.png")
                await channel.send(f"<@{author.id}>", file=map_image)
            return

        if content.startswith(f"<@{self.user.id}> !help"):
            await channel.send(
                f"<@{author.id}> Available commands:\n"
                f"`!hello`\n"
                f"`!ping`\n"
                f"`!map`\n"
            )
            return

        await channel.send(f"<@{author.id}> try `!help` command")


def main() -> None:
    intents = Intents.default()
    intents.message_content = True

    client = App(intents=intents, proxy=ConnectionConfig.PROXY_URL)
    client.run(BotConfig.BOT_TOKEN)


if __name__ == '__main__':
    main()

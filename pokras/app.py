from io import BytesIO

from PIL import Image
from discord import Intents, File
from discord.ext.commands import Cog, Context, command, Bot, check

from config import BotConfig, ConnectionConfig, DataConfig
from game.queries.create_game import create_game
from game.queries.get_game import get_active_game_by_channel_id, get_games_by_channel_id, get_game_by_id
from game.queries.update_game import set_game_inactive, set_game_active


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


class AppCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def list_games(self, ctx: Context):
        channel_id = ctx.channel.id
        games = get_games_by_channel_id(channel_id)
        response = "games:\n"
        for game in games:
            response += f"- {game.__repr__()}\n"
        await ctx.send(response)

    @command()
    @is_admin()
    async def create_game(self, ctx: Context):
        channel_id = ctx.channel.id
        game = get_active_game_by_channel_id(channel_id)

        if game:
            await ctx.send(f"an active game for this channel already exists: {game}")
            return

        game = create_game(channel_id)
        await ctx.send(f"game created: {game}")

    @command()
    @is_admin()
    async def stop_game(self, ctx: Context):
        channel_id = ctx.channel.id
        game = get_active_game_by_channel_id(channel_id)
        if not game:
            await ctx.send("there is no active game for this channel")
            return
        set_game_inactive(game.id)
        await ctx.send("game stopped")

    @command()
    @is_admin()
    async def start_game(self, ctx: Context, game_id: int):
        game = get_game_by_id(game_id)
        if not game:
            await ctx.send("game not found")
            return
        set_game_active(game.id)
        await ctx.send("game started")

    @command()
    async def map(self, ctx: Context):
        map_image = Image.open(DataConfig.RESOURCES / "map.png").convert('RGB')
        with BytesIO() as image_binary:
            map_image.save(image_binary, 'PNG')
            image_binary.seek(0)
            map_image = File(fp=image_binary, filename="map.png")
        await ctx.send(f"{ctx.author.mention}", file=map_image)


class App(Bot):
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("=" * 30)
        await self.add_cog(AppCommands(self))


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

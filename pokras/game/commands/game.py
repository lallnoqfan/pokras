from io import BytesIO

from PIL import Image
from discord import File
from discord.ext.commands import Cog, command, Context

from game.commands.checks import is_admin
from config import DataConfig
from game.queries.create_game import create_game
from game.queries.get_game import get_games_by_channel_id, get_active_game_by_channel_id, get_game_by_id
from game.queries.update_game import set_game_inactive, set_game_active
from game.responses.game import GameResponses


class GameCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def list_games(self, ctx: Context):
        """
        Возвращает список игр для текущего канала
        """
        channel_id = ctx.channel.id
        games = get_games_by_channel_id(channel_id)
        response = GameResponses.list_games(games)
        await ctx.send(response)

    @command()
    @is_admin()
    async def create_game(self, ctx: Context):
        """
        Создаёт новую игру в текущем канале
        """
        channel_id = ctx.channel.id
        game = get_active_game_by_channel_id(channel_id)
        if game:
            response = GameResponses.active_game_already_exists(game)
            await ctx.send(response)
            return

        game = create_game(channel_id)
        response = GameResponses.game_created(game)
        await ctx.send(response)

    @command()
    @is_admin()
    async def stop_game(self, ctx: Context):
        """
        Останавливает активную игру в текущем канале
        """
        channel_id = ctx.channel.id
        game = get_active_game_by_channel_id(channel_id)
        if not game:
            response = GameResponses.no_active_games()
            await ctx.send(response)
            return

        set_game_inactive(game.id)
        response = GameResponses.game_stopped(game)
        await ctx.send(response)

    @command()
    @is_admin()
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

        active_game = get_active_game_by_channel_id(ctx.channel.id)
        if active_game:
            response = GameResponses.active_game_already_exists(active_game)
            await ctx.send(response)
            return

        game = get_game_by_id(game_id)
        if not game:
            response = GameResponses.game_not_found()
            await ctx.send(response)
            return

        set_game_active(game.id)
        response = GameResponses.game_started(game)
        await ctx.send(response)

    @command()
    async def map(self, ctx: Context):
        """
        Постит карту (пустую (пока что (?)))
        """
        map_image = Image.open(DataConfig.RESOURCES / "map.png").convert('RGB')
        with BytesIO() as image_binary:
            map_image.save(image_binary, 'PNG')
            image_binary.seek(0)
            map_image = File(fp=image_binary, filename="map.png")
        await ctx.send(f"{ctx.author.mention}", file=map_image)

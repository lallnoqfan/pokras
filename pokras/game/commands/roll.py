from io import BytesIO

from discord import File
from discord.ext.commands import Cog, command, Context

from game.commands.checks import has_active_game
from game.queries.get_country import get_country_by_name, get_countries_by_game_id
from game.queries.get_game import get_active_game_by_channel_id
from game.responses.country import CountryResponses
from game.responses.roll import RollResponses
from game.utils.parser import CommentParser
from game.utils.randomizer import dices
from game.utils.resources import ResourcesHandler, CountryModel


class RollCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    @has_active_game()
    async def roll(self, ctx: Context, country_name: str | None, *prompt: str | None):
        """
        Args:
            country_name: название страны, за которую распределяются захваты
            prompt: распределение захватов. может быть:
                а) список тайлов (e.g. 1а 2bc 3деф)
                б) ролл против другой страны (e.g. "против швайнохаоситов",
                    если в игре есть страна с названием "швайнохаоситы")
                в) ролл на расширение по нейтральным территориям (e.g. "на расширение")

                "Против" и "на расширение" - ключевые слова для определения
                распределения захватов.
        """
        if not country_name:
            response = CountryResponses.missing_name()
            await ctx.reply(response)
            return

        game = get_active_game_by_channel_id(ctx.channel.id)
        country = get_country_by_name(game.id, country_name)
        if not country:
            response = CountryResponses.country_not_found(country_name)
            await ctx.reply(response)
            return

        if not prompt:
            response = RollResponses.missing_prompt()
            await ctx.reply(response)
            return

        roll = dices(ctx.message.id)
        roll_value = CommentParser.get_roll_value("".join(map(str, roll)))

        response = RollResponses.roll(roll, roll_value)

        if not roll_value:
            await ctx.reply(response)
            return

        prompt = " ".join(prompt)

        if CommentParser.is_roll_against(prompt):
            response += "ролл против"  # todo: add actual logic
            await ctx.reply(response)
            return

        if CommentParser.is_roll_on_neutral(prompt):
            response += "ролл на расширение"  # todo: add actual logic
            await ctx.reply(response)
            return

        tiles = CommentParser.process_tiles(prompt)
        response += f"\n({' '.join(tiles)})"  # todo: add actual logic

        await ctx.reply(response)

    @command()
    async def map(self, ctx: Context):
        """
        Постит карту активной игры
        """
        # todo: take game id as optional argument so it can be used not just for active game
        game = get_active_game_by_channel_id(ctx.channel.id)
        countries = get_countries_by_game_id(game.id)
        countries = [CountryModel(
            name=country.name,
            hex_color=country.color,
            tiles=[tile.code for tile in country.tiles],
        ) for country in countries]

        map_image = ResourcesHandler.draw_map(countries)

        with BytesIO() as image_binary:
            map_image.save(image_binary, 'PNG')
            image_binary.seek(0)
            map_image = File(fp=image_binary, filename="map.png")

        await ctx.reply(file=map_image)

    @command()
    @has_active_game()
    async def legend(self, ctx: Context):
        """
        Постит легенду стран в активной игре
        """
        # todo: take game id as optional argument so it can be used not just for active game
        game = get_active_game_by_channel_id(ctx.channel.id)
        countries = get_countries_by_game_id(game.id)
        countries = [CountryModel(
                name=country.name,
                hex_color=country.color,
                tiles=[tile.code for tile in country.tiles],
            ) for country in countries]

        countries_image = ResourcesHandler.draw_countries(countries)

        with BytesIO() as image_binary:
            countries_image.save(image_binary, 'PNG')
            image_binary.seek(0)
            countries_image = File(fp=image_binary, filename="countries.png")

        await ctx.reply(file=countries_image)

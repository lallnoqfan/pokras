from discord.ext.commands import (
    Bot,
    Cog,
    Context,
    group,
    command,
    guild_only,
    cooldown,
    BucketType,
    CheckFailure,
    CommandOnCooldown,
)

from game.commands.checks import has_active_game
from game.games.base.painter.country import Country
from game.games.base.parser.base_parser import BaseParser
from game.games.strategy import ServiceStrategy
from game.queries.get_country import get_country_by_name, get_countries_by_game_id
from game.queries.get_game import get_active_game_by_channel_id
from game.responses.country import CountryResponses
from game.responses.roll import RollResponses
from game.utils.discord import pillow_to_file
from game.utils.randomizer import dices


class RollCommands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @group(name="roll", aliases=["ролл"])
    @guild_only()
    @has_active_game()
    async def roll_group(self, ctx: Context):
        """
        5d10 ролл
        """
        if ctx.invoked_subcommand is None:
            await ctx.reply("try !help roll")

    @roll_group.command(name="tiles", aliases=["тайлы"])
    async def roll_tiles(self, ctx: Context, country_name: str | None, *tiles: str | None):
        """
        Ролл на список тайлов (e.g. 1а 2bc 3деф)

        Args:
            country_name: название страны, за которую распределяются захваты
            tiles: Список тайлов
        """
        if not country_name:
            response = CountryResponses.missing_name()
            await ctx.reply(response)
            return

        if not tiles:
            response = RollResponses.missing_tiles()
            await ctx.reply(response)
            return

        game = get_active_game_by_channel_id(ctx.channel.id)
        country = get_country_by_name(game.id, country_name)
        if not country:  # todo: move to service
            response = CountryResponses.country_not_found(country_name)
            await ctx.reply(response)
            return

        response = []

        roll = dices(ctx.message.id)
        roll_value = BaseParser.get_roll_value("".join(map(str, roll)))
        response.append(RollResponses.roll(roll, roll_value))

        tiles = " ".join(tiles)

        service = ServiceStrategy(game.map)
        remaining_roll_value, response_list = service.add_tiles(game, country, roll_value, tiles)

        response.extend(response_list)
        response = "\n" + "\n".join(response)
        await ctx.reply(response)

        if remaining_roll_value != roll_value:
            # todo: this should not work this hardcoded-like way
            #       later it will be great to separate all map render logic out of endpoint
            await ctx.invoke(self.map)

    @roll_group.command(name="expansion", aliases=["покрас", "расширение"])
    async def roll_expansion(self, ctx: Context, country_name: str | None):
        """
        Ролл на расширение по нейтральным территориям.
        Наролленные захваты распределяются по доступным нейтральным территориям, если такие есть.
        """
        if not country_name:
            response = CountryResponses.missing_name()
            await ctx.reply(response)
            return

        game = get_active_game_by_channel_id(ctx.channel.id)
        country = get_country_by_name(game.id, country_name)
        if not country:  # todo: move to service
            response = CountryResponses.country_not_found(country_name)
            await ctx.reply(response)
            return

        response = []

        roll = dices(ctx.message.id)
        roll_value = BaseParser.get_roll_value("".join(map(str, roll)))
        response.append(RollResponses.roll(roll, roll_value))

        service = ServiceStrategy(game.map)
        remaining_roll_value, response_list = service.add_expansion(game, country, roll_value)

        if remaining_roll_value:  # todo: move to service
            response_list.append(RollResponses.roll_value_surplus(remaining_roll_value))
        response.extend(response_list)
        response = "\n" + "\n".join(response)
        await ctx.reply(response)

        if remaining_roll_value != roll_value:
            # todo: this should not work this hardcoded-like way
            #       later it will be great to separate all map render logic out of endpoint
            await ctx.invoke(self.map)

    @roll_group.command(name="against", aliases=["против"])
    async def roll_against(self, ctx: Context, country_name: str | None, target_name: str | None):
        """
        Ролл против другой страны
        (e.g. "против швайнохаоситов", если в игре есть страна с названием "швайнохаоситы")
        """
        if not country_name:
            response = CountryResponses.missing_name()
            await ctx.reply(response)
            return

        if not target_name:
            response = RollResponses.missing_target()
            await ctx.reply(response)
            return

        game = get_active_game_by_channel_id(ctx.channel.id)
        country = get_country_by_name(game.id, country_name)
        if not country:  # todo: move to service
            response = CountryResponses.country_not_found(country_name)
            await ctx.reply(response)
            return
        target = get_country_by_name(game.id, target_name)
        if not target:
            response = CountryResponses.country_not_found(target_name)
            await ctx.reply(response)
            return
        response = []

        roll = dices(ctx.message.id)
        roll_value = BaseParser.get_roll_value("".join(map(str, roll)))
        response.append(RollResponses.roll(roll, roll_value))

        service = ServiceStrategy(game.map)
        remaining_roll_value, response_list = service.add_against(game, country, target, roll_value)

        if remaining_roll_value:  # todo: move to service
            response_list.append(RollResponses.roll_value_surplus(remaining_roll_value))
        response.extend(response_list)
        response = "\n" + "\n".join(response)
        await ctx.reply(response)

        if remaining_roll_value != roll_value:
            # todo: this should not work this hardcoded-like way
            #       later it will be great to separate all map render logic out of endpoint
            await ctx.invoke(self.map)

    @command()
    @guild_only()
    @has_active_game()
    @cooldown(1, 30, BucketType.channel)
    async def map(self, ctx: Context):
        """
        Постит карту активной игры
        """
        # todo: take game id as optional argument so it can be used not just for active game
        game = get_active_game_by_channel_id(ctx.channel.id)
        countries = get_countries_by_game_id(game.id)

        service = ServiceStrategy(game.map)
        painter = service.painter
        tiler = service.tiler

        countries = [Country(
            name=country.name,
            hex_color=country.color,
            tiles=[tile.code for tile in country.tiles],
        ) for country in countries]

        map_image = painter.draw_map(tiler, countries)

        map_file = pillow_to_file(map_image, "map.png")
        await ctx.reply(file=map_file)

    @map.error
    async def map_error(self, ctx: Context, error: Exception):
        if isinstance(error, CheckFailure):
            pass

        elif isinstance(error, CommandOnCooldown):
            await ctx.reply("You can only use this command once every 30 seconds per channel.")

        else:
            raise error

    @command()
    @guild_only()
    @has_active_game()
    @cooldown(1, 30, BucketType.channel)
    async def legend(self, ctx: Context):
        """
        Постит легенду стран в активной игре
        """
        # todo: take game id as optional argument so it can be used not just for active game
        # but then we would need to check if user is admin of that game... or smth idk
        game = get_active_game_by_channel_id(ctx.channel.id)
        countries = get_countries_by_game_id(game.id)
        if not countries:
            await ctx.reply("There are no countries in this game, so... no legend i guess?")
            return

        service = ServiceStrategy(game.map)
        painter = service.painter
        tiler = service.tiler

        countries = [Country(
            name=country.name,
            hex_color=country.color,
            tiles=[tile.code for tile in country.tiles],
        ) for country in countries]

        legend_image = painter.draw_legend(tiler, countries)
        countries_file = pillow_to_file(legend_image, "legend.png")
        await ctx.reply(file=countries_file)

    @legend.error
    async def legend_error(self, ctx: Context, error: Exception):
        if isinstance(error, CheckFailure):
            pass

        elif isinstance(error, CommandOnCooldown):
            await ctx.reply("You can only use this command once every 30 seconds per channel.")

        else:
            raise error

from discord.ext.commands import Cog, command, Context, guild_only

from game.commands.checks import has_active_game
from game.queries.create_country import create_country
from game.queries.get_country import get_country_by_color, get_country_by_name, get_countries_by_game_id
from game.queries.get_game import get_active_game_by_channel_id
from game.queries.update_country import set_country_name, set_country_color
from game.responses.country import CountryResponses
from game.utils.parser import CommentParser


class CountryCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    @guild_only()
    @has_active_game()
    async def create_country(self, ctx: Context, color: str, *name: str | None):
        """
        Создаёт страну в активной игре

        Args:
            color: Цвет новой страны в hex формате (e.g. #ff0000 или #F00 (или даже #ф00))
            name: Название новой страны
        """

        if not name:
            response = CountryResponses.missing_name()
            await ctx.send(response)
            return

        name: str = " ".join(name)

        if not color:
            response = CountryResponses.missing_color()
            await ctx.send(response)
            return

        color = CommentParser.parse_color(color)
        if not color:
            response = CountryResponses.invalid_color(color)
            await ctx.reply(response)
            return

        game = get_active_game_by_channel_id(ctx.channel.id)
        country = get_country_by_color(game.id, color)
        if country:
            response = CountryResponses.color_already_exists(country)
            await ctx.send(response)
            return

        country = get_country_by_name(game.id, name)
        if country:
            response = CountryResponses.name_already_exists(country)
            await ctx.send(response)
            return

        country = create_country(name, color, game.id, ctx.author.id)
        response = CountryResponses.country_created(country)
        await ctx.send(response)

    @command()
    @guild_only()
    @has_active_game()
    async def change_name(self, ctx: Context, old_name: str | None, new_name: str | None):
        """
        Переименовывает страну в активной игре
        Только создатель страны может переименовывать её

        Args:
            old_name: Старое название страны
            new_name: Новое название страны
        """
        if not old_name:
            response = CountryResponses.missing_name()
            await ctx.send(response)
            return

        if not new_name:
            response = CountryResponses.missing_new_name()
            await ctx.send(response)
            return

        game = get_active_game_by_channel_id(ctx.channel.id)
        country = get_country_by_name(game.id, new_name)
        if country:
            response = CountryResponses.new_name_already_exists(country)
            await ctx.send(response)
            return

        country = get_country_by_name(game.id, old_name)
        if not country:
            response = CountryResponses.country_not_found(old_name)
            await ctx.send(response)
            return

        if (country.creator_id != ctx.author.id
                and ctx.guild is not None
                and not ctx.author.guild_permissions.administrator):
            response = CountryResponses.not_creator(country)
            await ctx.send(response)
            return

        set_country_name(game.id, country.id, new_name)
        response = CountryResponses.name_changed(country)
        await ctx.send(response)

    @command()
    @guild_only()
    @has_active_game()
    async def change_color(self, ctx: Context, country_name: str | None, new_color: str | None):
        """
        Изменяет цвет страны в активной игре

        Args:
            country_name: Название страны
            new_color: Новый цвет страны (в HEX-формате)
        """
        if not country_name:
            response = CountryResponses.missing_name()
            await ctx.send(response)
            return

        if not new_color:
            response = CountryResponses.missing_new_color()
            await ctx.send(response)
            return

        new_color = CommentParser.parse_color(new_color)
        if not new_color:
            response = CountryResponses.invalid_color(new_color)
            await ctx.reply(response)
            return

        game = get_active_game_by_channel_id(ctx.channel.id)
        country = get_country_by_name(game.id, country_name)
        if not country:
            response = CountryResponses.country_not_found(country_name)
            await ctx.send(response)
            return

        if (country.creator_id != ctx.author.id
                and ctx.guild is not None
                and not ctx.author.guild_permissions.administrator):
            response = CountryResponses.not_creator(country)
            await ctx.send(response)
            return

        set_country_color(game.id, country.id, new_color)
        response = CountryResponses.color_changed(country)
        await ctx.send(response)

    @command()
    @guild_only()
    @has_active_game()
    async def list_countries(self, ctx: Context):
        """
        Возвращает список стран в активной игре
        """
        game = get_active_game_by_channel_id(ctx.channel.id)
        countries = get_countries_by_game_id(game.id)
        response = CountryResponses.list_countries(countries)
        await ctx.send(response)

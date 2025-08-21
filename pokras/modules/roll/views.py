from discord.ext.commands import Cog, Bot, group, guild_only, Context, command, cooldown, BucketType, CheckFailure, \
    CommandOnCooldown

from modules.country.queries.get_country import get_country_by_name, get_countries_by_game_id
from modules.country.responses import CountryResponses
from modules.game.queries.get_game import get_active_game_by_channel_id
from modules.roll.responses import RollResponses
from modules.roll.service.base.models.prompt import Prompt
from modules.roll.service.strategy import ServiceStrategy
from utils.checks import has_active_game
from utils.discord import pillow_to_file
from utils.random import dices
from utils.text import Tags as T


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

        roll = dices(ctx.message.id)
        tiles = " ".join(tiles)

        service = ServiceStrategy(game)
        service_response = service.add_tiles(game, country, Prompt(
            roll=roll, timestamp=ctx.message.created_at,
        ), tiles)
        response = service_response.messages
        state_changed = service_response.map_state_changed

        response = "\n" + "\n".join(response)
        await ctx.reply(response)

        if state_changed:
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

        roll = dices(ctx.message.id)

        service = ServiceStrategy(game)
        service_response = service.add_expansion(game, country, Prompt(
            roll=roll, timestamp=ctx.message.created_at,
        ))
        response = service_response.messages
        state_changed = service_response.map_state_changed

        response = "\n" + "\n".join(response)
        await ctx.reply(response)

        if state_changed:
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

        roll = dices(ctx.message.id)

        service = ServiceStrategy(game)
        service_response = service.add_against(game, country, Prompt(
            roll=roll, timestamp=ctx.message.created_at,
        ), target)
        response = service_response.messages
        state_changed = service_response.map_state_changed

        response = "\n" + "\n".join(response)
        await ctx.reply(response)

        if state_changed:
            # todo: this should not work this hardcoded-like way
            #       later it will be great to separate all map render logic out of endpoint
            await ctx.invoke(self.map)

    @command(name="артефакты")
    async def roll_artifacts(self, ctx: Context, artifact_sites: int):
        """
        Ролл на артефакты с подсветкой дропа

        Args:
            artifact_sites: количество точек сбора артефактов
        """
        ARTIFACTS = {
            1: ['Медуза (М)', 'Каменный цветок (КЦ)', 'Ночная звезда (НЗ)'],
            3: ['Бенгальский огонь (БО)', 'Вспышка (В)', 'Лунный свет (ЛС)'],
            5: ['Кровь камня (КК)', 'Ломоть мяса (ЛМ)', 'Душа (Д)'],
            7: ['Капли (К)', 'Огненный шар (ОШ)', 'Кристалл (КТ)'],
            9: ['Колючка (КЧ)', 'Кристальная волочка (ККЧ)', 'Морской ёж (МЁ)'],
        }
        RARE_ARTIFACTS = {
            '2 2': 'Колобок',
            '4 4': 'Пружина',
            '6 6': 'Пустышка',
            '8 8': 'Мамины бусы',
            '0 0': 'Плёнка',
            '7 6 7': 'Батарейка',
            '6 7 6': 'Компас',
        }
        ROLL_QUALITY = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 1,
            6: 1,
            7: 1,
            8: 2,
            9: 2,
        }

        seed = ctx.message.id
        num_rolls = artifact_sites * 2
        roll = dices(seed, num_rolls)

        messages = [" ".join(map(lambda n: T.code(str(n)), roll)), ""]
        even_numbers = roll[0::2]
        odd_numbers = roll[1::2]

        for artifact_quality, artifact_class in zip(even_numbers, odd_numbers):
            message = f"{T.code(f'{artifact_quality}')} {T.code(f'{artifact_class}')} — "
            if artifact_class == 0:
                message += "потеря точки"
            elif artifact_class % 2 == 0:
                message += "нет артефакта"
            elif artifact_quality == 0:
                message += "нет артефакта"
            else:
                artifact_quality = ROLL_QUALITY[artifact_quality]
                artifact = ARTIFACTS[artifact_class][artifact_quality]
                message += artifact
            messages.append(message)
        messages.append("")

        if artifact_sites < 3:
            message = "Недостаточно точек для сбора редких артефактов..."
            messages.append(message)

        else:
            key_str = " ".join(map(str, roll))
            for rare_prompt in RARE_ARTIFACTS:
                if rare_prompt in key_str:
                    message = f"{T.code(rare_prompt)} — {RARE_ARTIFACTS[rare_prompt]}"
                    messages.append(message)

        response = "\n".join(messages)
        await ctx.reply(response)

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

        service = ServiceStrategy(game)
        painter = service.painter
        tiler = service.tiler

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

        service = ServiceStrategy(game)
        painter = service.painter
        tiler = service.tiler

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

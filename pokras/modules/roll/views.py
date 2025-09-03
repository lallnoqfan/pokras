from discord.ext.commands import Cog, Bot, group, guild_only, Context, command, cooldown, BucketType, CheckFailure, \
    CommandOnCooldown, BadArgument, MissingRequiredArgument

from modules.country.queries.get_country import get_countries_by_game_id
from modules.game.queries.get_game import get_active_game_by_channel_id
from modules.roll.service.base.models.api_things import AgainstRollPrompt, ExpansionRollPrompt, TilesRollPrompt
from modules.roll.service.strategy import ServiceFactory
from utils.checks import has_active_game
from utils.discord import pillow_to_file, cv2_to_file
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
            await ctx.send_help("roll")

    @roll_group.command(name="tiles", aliases=["тайлы"])
    async def roll_tiles(self, ctx: Context, country_name: str, *tiles: str):
        """
        Ролл на список тайлов (e.g. 1а 2bc 3деф)

        Args:
            country_name: название страны, за которую распределяются захваты
            tiles: Список тайлов
        """
        game = get_active_game_by_channel_id(ctx.channel.id)
        roll = dices(ctx.message.id)
        tiles = list(tiles)

        service = ServiceFactory.build_service(game)
        service_response = service.add_tiles(game.cast(), TilesRollPrompt(
            roll=roll, timestamp=ctx.message.created_at, country=country_name, tiles=tiles,
            roll_value=0,
        ))
        response = service_response.messages
        state_changed = service_response.map_state_changed

        response = "\n" + "\n".join(response)
        await ctx.reply(response)

        if state_changed:
            await ctx.invoke(self.draw_map)

    @roll_tiles.error
    async def roll_tiles_error(self, ctx: Context, error: Exception):
        if isinstance(error, MissingRequiredArgument):
            response = f"{error.param.name} is missing"
            await ctx.reply(response)

        elif isinstance(error, CheckFailure):
            pass

        else:
            response = f"{type(error)}: {error}"
            await ctx.reply(response)
            raise error

    @roll_group.command(name="expansion", aliases=["покрас", "расширение"])
    async def roll_expansion(self, ctx: Context, country_name: str):
        """
        Ролл на расширение по нейтральным территориям.
        Наролленные захваты распределяются по доступным нейтральным территориям, если такие есть.
        """
        game = get_active_game_by_channel_id(ctx.channel.id)
        roll = dices(ctx.message.id)

        service = ServiceFactory.build_service(game)
        service_response = service.add_expansion(game.cast(), ExpansionRollPrompt(
            roll=roll, timestamp=ctx.message.created_at, country=country_name,
            roll_value=0,
        ))
        response = service_response.messages
        state_changed = service_response.map_state_changed

        response = "\n" + "\n".join(response)
        await ctx.reply(response)

        if state_changed:
            await ctx.invoke(self.draw_map)

    @roll_expansion.error
    async def roll_expansion_error(self, ctx: Context, error: Exception):
        if isinstance(error, MissingRequiredArgument):
            response = f"{error.param.name} is missing"
            await ctx.reply(response)

        elif isinstance(error, CheckFailure):
            pass

        else:
            response = f"{type(error)}: {error}"
            await ctx.reply(response)
            raise error

    @roll_group.command(name="against", aliases=["против"])
    async def roll_against(self, ctx: Context, country_name: str, target_name: str):
        """
        Ролл против другой страны
        (e.g. "против швайнохаоситов", если в игре есть страна с названием "швайнохаоситы")
        """
        game = get_active_game_by_channel_id(ctx.channel.id)
        roll = dices(ctx.message.id)

        service = ServiceFactory.build_service(game)
        service_response = service.add_against(game.cast(), AgainstRollPrompt(
            roll=roll, timestamp=ctx.message.created_at, country=country_name, target=target_name,
            roll_value=0,
        ))
        response = service_response.messages
        state_changed = service_response.map_state_changed

        response = "\n" + "\n".join(response)
        await ctx.reply(response)

        if state_changed:
            await ctx.invoke(self.draw_map)

    @roll_against.error
    async def roll_against_error(self, ctx: Context, error: Exception):
        if isinstance(error, MissingRequiredArgument):
            response = f"{error.param.name} is missing"
            await ctx.reply(response)

        elif isinstance(error, CheckFailure):
            pass

        else:
            response = f"{type(error)}: {error}"
            await ctx.reply(response)
            raise error

    @command(name="артефакты")
    async def roll_artifacts(self, ctx: Context, artifact_sites: int):
        """
        Ролл на артефакты с подсветкой дропа

        Args:
            artifact_sites: количество точек сбора артефактов
        """
        if artifact_sites < 0:
            await ctx.reply(f"{artifact_sites}? фо рил?")
            return

        if artifact_sites > 40:
            await ctx.reply("на карте столько точек нет шизоидище")
            return

        ARTIFACTS = {
            1: ['Медуза (М)', 'Каменный цветок (КЦ)', 'Ночная звезда (НЗ)'],
            3: ['Бенгальский огонь (БО)', 'Вспышка (В)', 'Лунный свет (ЛС)'],
            5: ['Кровь камня (КК)', 'Ломоть мяса (ЛМ)', 'Душа (Д)'],
            7: ['Капли (К)', 'Огненный шар (ОШ)', 'Кристалл (КТ)'],
            9: ['Колючка (КЧ)', 'Кристальная колючка (ККЧ)', 'Морской ёж (МЁ)'],
        }
        RARE_ARTIFACTS = {
            '2 2': 'Колобок',
            '4 4': 'Пружина',
            '6 6': 'Пустышка',
            '8 8': 'Мамины бусы',
            '0 0': 'Плёнка',
            '1 2 1': 'Батарейка',
            '9 8 9': 'Компас',
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
                count = key_str.count(rare_prompt)
                if count:
                    message = (f"{T.code(rare_prompt)} — "
                               f"{f'{count}x ' if count > 1 else ''}{RARE_ARTIFACTS[rare_prompt]}")
                    messages.append(message)

        response = "\n".join(messages)
        await ctx.reply(response)

    @roll_artifacts.error
    async def roll_artifacts_error(self, ctx: Context, error: Exception):
        if isinstance(error, MissingRequiredArgument):
            response = f"{error.param.name} is missing"
            await ctx.reply(response)

        if isinstance(error, BadArgument):
            await ctx.reply("RTFM")
            await ctx.send_help("артефакты")

        else:
            response = f"{type(error)}: {error}"
            await ctx.reply(response)
            raise error

    @command(name="map")
    @guild_only()
    @has_active_game()
    @cooldown(1, 30, BucketType.channel)
    async def draw_map(self, ctx: Context):
        """
        Постит карту активной игры
        """
        # todo: take game id as optional argument so it can be used not just for active game
        game = get_active_game_by_channel_id(ctx.channel.id)
        countries = get_countries_by_game_id(game.id)
        countries = list(map(lambda country: country.cast(), countries))

        service = ServiceFactory.build_service(game)
        painter = service.painter
        tiler = service.tiler
        repository = service.repository

        map_image = painter.draw_map(countries, tiler, repository)

        map_file = cv2_to_file(map_image, "map.png")
        await ctx.reply(file=map_file)

    @draw_map.error
    async def draw_map_error(self, ctx: Context, error: Exception):
        if isinstance(error, CheckFailure):
            pass

        elif isinstance(error, CommandOnCooldown):
            await ctx.reply("You can only use this command once every 30 seconds per channel.")

        else:
            response = f"{type(error)}: {error}"
            await ctx.reply(response)
            raise error

    @command(name="legend")
    @guild_only()
    @has_active_game()
    @cooldown(1, 30, BucketType.channel)
    async def draw_legend(self, ctx: Context):
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
        countries = list(map(lambda country: country.cast(), countries))

        service = ServiceFactory.build_service(game)
        painter = service.painter
        tiler = service.tiler
        repository = service.repository

        legend_image = painter.draw_legend(countries, tiler, repository)
        countries_file = pillow_to_file(legend_image, "legend.png")
        await ctx.reply(file=countries_file)

    @draw_legend.error
    async def draw_legend_error(self, ctx: Context, error: Exception):
        if isinstance(error, CheckFailure):
            pass

        elif isinstance(error, CommandOnCooldown):
            await ctx.reply("You can only use this command once every 30 seconds per channel.")

        else:
            response = f"{type(error)}: {error}"
            await ctx.reply(response)
            raise error

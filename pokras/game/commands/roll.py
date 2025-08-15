from collections import defaultdict

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
from game.queries.create_tile import create_tile
from game.queries.get_country import get_country_by_name, get_countries_by_game_id
from game.queries.get_game import get_active_game_by_channel_id
from game.queries.get_tile import get_tile
from game.queries.update_tile import update_tile_owner
from game.responses.country import CountryResponses
from game.responses.roll import RollResponses
from game.tables import Country, Game
from game.utils.discord import pillow_to_file
from game.utils.parser import CommentParser
from game.utils.randomizer import dices
from game.utils.resources import ResourcesHandler, CountryModel


# all that stuff might be quite slow... should consider adding db locks


class RollCommands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def _add_tiles(roll_value: int, game: Game, country: Country, tile_codes: list[str],
                   resources: type[ResourcesHandler]) -> tuple[int, list[str]]:
        # that's some serious spaghetti... probably even doesn't work lmfao
        # i'm too scared now to even try to decompose it
        #
        # not so scary now, i'll rework it, just two more weeks

        response = []

        # check if tile exists
        updated_tiles = []
        for tile_code in tile_codes:
            if not resources.tile_exists(tile_code):
                print(f"{tile_code} is invalid")
                # todo: should try to implement bulk response so all tiles are mentioned by one line
                #       for now that "tile is invalid x9000" spam just feels annoying
                response.append(RollResponses.invalid_tile(tile_code))
            else:
                updated_tiles.append(tile_code)
        tile_codes = updated_tiles

        # check if player owns tile
        updated_tiles = []
        for tile_code in tile_codes:
            tile = get_tile(tile_code, game.id)
            if tile is not None and tile.owner_id == country.id:
                response.append(RollResponses.capture_owned(tile_code))
            else:
                updated_tiles.append(tile_code)
        tile_codes = updated_tiles

        # if country has no tiles
        if not country.tiles:
            tile_code = tile_codes.pop(0)
            tile = get_tile(tile_code, game.id)

            # free spot spawn
            if tile is None:
                response.append(RollResponses.spawn(country.name, tile_code))
                create_tile(tile_code, game.id, country.id)

            elif tile.owner is None:
                # nukes currently don't exist, so technically there is no way
                # for an existing in db tile to have no owner
                # though it's a good idea to check it since further updates
                # might change something
                # anyway, live by cursed project structure, die by it...
                # also, i should probably extract this checks
                # to somewhere to make these statements more readable...
                # but whatever for now
                #
                # this thing just should not rely on db entries...
                response.append(RollResponses.spawn(country.name, tile_code))
                update_tile_owner(game.id, tile_code, country.id)

            # attack spawn
            else:
                attacked: Country = tile.owner
                response.append(RollResponses.spawn_attack(country.name, tile_code, attacked.name))
                update_tile_owner(game.id, tile_code, country.id)

            roll_value -= 1

        # if country has tiles
        while roll_value > 0 and tile_codes:

            # now the hard(?) part. since not all tiles might be reachable from input order,
            # but with capturing other tiles they might become reachable,
            # we need to check them all again and again while there is still some roll value

            were_captures = False
            owned_tiles = set(tile.code for tile in country.tiles)

            for tile_code in tile_codes:
                for adjacent_tile in resources.get_tile(tile_code).get("routes"):
                    if adjacent_tile not in owned_tiles:
                        continue
                    were_captures = True

                    tile = get_tile(tile_code, game.id)

                    if tile is None:
                        response.append(RollResponses.capture_neutral(country.name, tile_code))
                        create_tile(tile_code, game.id, country.id)

                    elif tile.owner is None:
                        response.append(RollResponses.capture_neutral(country.name, tile_code))
                        update_tile_owner(game.id, tile_code, country.id)

                    else:
                        attacked: Country = tile.owner  # noqa: shut up
                        response.append(RollResponses.capture_attack(country.name, tile_code, attacked.name))
                        update_tile_owner(game.id, tile_code, country.id)

                    tile_codes.remove(tile_code)
                    roll_value -= 1
                    break

                if were_captures:
                    break
            if were_captures:
                continue

            # no connected tiles remaining
            for tile_code in tile_codes:  # and there is still some roll value
                response.append(RollResponses.capture_no_route(tile_code))
            break

        return roll_value, response

    @staticmethod
    def _add_tiles_expansion(roll_value: int, game: Game, country: Country,
                             resources: type[ResourcesHandler]) -> tuple[int, list[str]]:
        # this thing chooses somewhat nearest tiles to the country
        # the way it interprets the "nearest" though is kinda not the best one
        #
        # it calcs distances between country's tiles and adjacent to them tiles
        # and then picks the closest adjacent tile to one of the country's tiles
        #
        # it leads to not what you would call "nearest" tiles selection pattern
        # maybe some other way like picking the closest neutral tile to mass centroid of the country
        # would do the job better
        #
        # but for now i don't care
        response = []

        if not country.tiles:
            response.append(RollResponses.expansion_without_tiles())
            return roll_value, response

        free_tiles_codes = defaultdict(lambda: float("inf"))
        visited = set()

        while roll_value > 0:
            # damn thats should be expensive server resources wise
            # ...
            # so ive checked this code, and actually, after we added one tile to the country
            # we would check ALL ITS TILES again for like nothing 'cause we only need to check ONE added tile...
            # yeah, i know that all visited tiles are already in the set, so it wouldn't take that long
            # but still some queue-ish structure would be really nice
            for tile in country.tiles:
                tile_code = tile.code
                if tile_code in visited:
                    continue
                visited.add(tile_code)

                adjacent_tiles = resources.get_adjacent_tiles(tile_code)
                for adjacent_tile_code in adjacent_tiles:
                    adjacent_tile = get_tile(adjacent_tile_code, game.id)
                    if adjacent_tile is not None and adjacent_tile.owner_id is not None:
                        continue

                    distance = resources.calc_distance(tile_code, adjacent_tile_code)
                    free_tiles_codes[adjacent_tile_code] = min(free_tiles_codes[adjacent_tile_code], distance)

            if not free_tiles_codes:
                break

            print(free_tiles_codes)
            nearest_tile_code = min(free_tiles_codes, key=free_tiles_codes.get)
            nearest_tile = get_tile(nearest_tile_code, game.id)
            # once again, it should not rely on db here
            if nearest_tile is None:
                create_tile(nearest_tile_code, game.id, country.id)
            else:
                update_tile_owner(game.id, nearest_tile_code, country.id)

            roll_value -= 1
            free_tiles_codes.pop(nearest_tile_code)
            response.append(RollResponses.capture_neutral(country.name, nearest_tile_code))

        if roll_value > 0:
            response.append(RollResponses.expansion_no_free_tiles())

        return roll_value, response

    @staticmethod
    def _add_tiles_against(roll_value: int, game: Game, country: Country, target: Country,
                           resources: type[ResourcesHandler]) -> tuple[int, list[str]]:
        # works pretty much in the same way as _add_tiles_expansion
        response = []

        if not country.tiles:
            response.append(RollResponses.against_without_tiles())
            return roll_value, response

        if not target.tiles:
            response.append(RollResponses.against_target_has_no_tiles(target.name))
            return roll_value, response

        if country.name == target.name:
            response.append(RollResponses.against_self())
            return roll_value, response

        target_tiles = defaultdict(lambda: float("inf"))
        visited = set()

        while roll_value > 0:
            for tile in country.tiles:
                tile_code = tile.code
                if tile_code in visited:
                    continue
                visited.add(tile_code)

                for adjacent_tile_code in resources.get_adjacent_tiles(tile_code):
                    adjacent_tile = get_tile(adjacent_tile_code, game.id)
                    if adjacent_tile is None or adjacent_tile.owner_id is not target.id:
                        continue

                    distance = resources.calc_distance(tile_code, adjacent_tile_code)
                    target_tiles[adjacent_tile_code] = min(target_tiles[adjacent_tile_code], distance)

            if not target_tiles:
                break

            nearest = min(target_tiles, key=target_tiles.get)
            update_tile_owner(game.id, nearest, country.id)
            roll_value -= 1
            target_tiles.pop(nearest)
            response.append(RollResponses.capture_attack(country.name, nearest, target.name))

        if roll_value > 0:
            response.append(RollResponses.against_no_routes(target.name))

        return roll_value, response

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
        if not country:
            response = CountryResponses.country_not_found(country_name)
            await ctx.reply(response)
            return

        roll = dices(ctx.message.id)
        roll_value = CommentParser.get_roll_value("".join(map(str, roll)))

        response = RollResponses.roll(roll, roll_value)

        if not roll_value:
            # don't really like this return statement here...
            # should consider a way to check if prompt is valid before sending response
            await ctx.reply(response)
            return

        tiles = " ".join(tiles)
        tiles = CommentParser.process_tiles(tiles)
        resources = ResourcesHandler(game.map)
        remaining_roll_value, response_list = self._add_tiles(roll_value, game, country, tiles, resources)
        if remaining_roll_value:
            response_list.append(RollResponses.roll_value_surplus(remaining_roll_value))
        response += "\n" + "\n".join(response_list)
        response += "\n(" + " ".join(tiles) + ")"

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
        if not country:
            response = CountryResponses.country_not_found(country_name)
            await ctx.reply(response)
            return

        roll = dices(ctx.message.id)
        roll_value = CommentParser.get_roll_value("".join(map(str, roll)))

        response = RollResponses.roll(roll, roll_value)

        if not roll_value:
            # don't really like this return statement here...
            # should consider a way to check if prompt is valid before sending response
            await ctx.reply(response)
            return

        resources = ResourcesHandler(game.map)
        remaining_roll_value, response_list = self._add_tiles_expansion(roll_value, game, country, resources)
        if remaining_roll_value:
            response_list.append(RollResponses.roll_value_surplus(remaining_roll_value))
        response += "\n" + "\n".join(response_list)

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
        if not country:
            response = CountryResponses.country_not_found(country_name)
            await ctx.reply(response)
            return
        target = get_country_by_name(game.id, target_name)
        if not target:
            response = CountryResponses.country_not_found(target_name)
            await ctx.reply(response)
            return

        roll = dices(ctx.message.id)
        roll_value = CommentParser.get_roll_value("".join(map(str, roll)))

        response = RollResponses.roll(roll, roll_value)

        if not roll_value:
            # don't really like this return statement here...
            # should consider a way to check if prompt is valid before sending response
            await ctx.reply(response)
            return

        resources = ResourcesHandler(game.map)
        remaining_roll_value, response_list = self._add_tiles_against(roll_value, game, country, target, resources)
        if remaining_roll_value:
            response_list.append(RollResponses.roll_value_surplus(remaining_roll_value))
        response += "\n" + "\n".join(response_list)

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
        resources = ResourcesHandler(game.map)

        if countries:
            countries = [CountryModel(
                name=country.name,
                hex_color=country.color,
                tiles=[tile.code for tile in country.tiles],
            ) for country in countries]

            map_image = resources.draw_map(countries)

        else:
            map_image = resources.load_map()

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
        resources = ResourcesHandler(game.map)

        countries = [CountryModel(
                name=country.name,
                hex_color=country.color,
                tiles=[tile.code for tile in country.tiles],
            ) for country in countries]

        countries_image = resources.draw_countries(countries)
        countries_file = pillow_to_file(countries_image, "countries.png")
        await ctx.reply(file=countries_file)

    @legend.error
    async def legend_error(self, ctx: Context, error: Exception):
        if isinstance(error, CheckFailure):
            pass

        elif isinstance(error, CommandOnCooldown):
            await ctx.reply("You can only use this command once every 30 seconds per channel.")

        else:
            raise error

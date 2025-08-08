from discord.ext.commands import Cog, command, Context, guild_only

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
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def _add_tiles(roll_value: int, game: Game, country: Country, tile_codes: list[str]) -> tuple[int, list[str]]:
        # that's some serious spaghetti... probably even doesn't work lmfao
        # i'm too scared now to even try to decompose it

        response = []

        # check if tile exists
        updated_tiles = []
        for tile_code in tile_codes:
            if not ResourcesHandler.tile_exists(tile_code):
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
            for tile_code in tile_codes:
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

                if tile in tile_codes:
                    tile_codes.remove(tile)
                roll_value -= 1

                break  # since now country has at least one tile

        # if country has tiles
        while roll_value > 0 and tile_codes:

            # now the hard(?) part. since not all tiles might be reachable from input order,
            # but with capturing other tiles they might become reachable,
            # we need to check them all again and again while there is still some roll value

            were_captures = False
            owned_tiles = set(tile.code for tile in country.tiles)

            for tile_code in tile_codes:
                for adjacent_tile in ResourcesHandler.get_tile(tile_code).get("routes"):
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

    @command()
    @guild_only()
    @has_active_game()
    async def roll(self, ctx: Context, country_name: str | None, *prompt: str | None):
        """
        Args:
            country_name: название страны, за которую распределяются захваты
            prompt: метод распределения захватов. может быть *одним из*:
                а) ролл на тайлы (e.g. 1а 2bc 3деф)

                wip (пока не работают):
                б) ролл против другой страны (e.g. "против швайнохаоситов",
                   если в игре есть страна с названием "швайнохаоситы")
                в) ролл на расширение по нейтральным территориям (e.g. "на расширение")

                "Против" и "расширение" - ключевые слова для определения
                распределения захватов.
        """
        if not country_name:
            response = CountryResponses.missing_name()
            await ctx.reply(response)
            return

        if not prompt:
            response = RollResponses.missing_prompt()
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

        prompt = " ".join(prompt)

        if CommentParser.is_roll_against(prompt):
            response += "\nролл против"  # todo: add actual logic

            await ctx.reply(response)
            return

        if CommentParser.is_roll_on_neutral(prompt):
            response += "\nролл на расширение"  # todo: add actual logic

            await ctx.reply(response)
            return

        tiles = CommentParser.process_tiles(prompt)
        remaining_roll_value, response_list = self._add_tiles(roll_value, game, country, tiles)
        if remaining_roll_value:
            response_list.append(RollResponses.roll_value_surplus(remaining_roll_value))
        response += "\n" + "\n".join(response_list)
        response += "\n(" + " ".join(tiles) + ")"

        await ctx.reply(response)

        if remaining_roll_value != roll_value:
            # todo: this should not work this hardcoded-like way
            #       later it will be great to separate all map render logic out of endpoint
            await ctx.invoke(self.bot.get_command("map"))

    @command()
    @guild_only()
    @has_active_game()
    async def map(self, ctx: Context):
        """
        Постит карту активной игры
        """
        # todo: take game id as optional argument so it can be used not just for active game
        game = get_active_game_by_channel_id(ctx.channel.id)
        countries = get_countries_by_game_id(game.id)

        if countries:
            countries = [CountryModel(
                name=country.name,
                hex_color=country.color,
                tiles=[tile.code for tile in country.tiles],
            ) for country in countries]

            map_image = ResourcesHandler.draw_map(countries)

        else:
            map_image = ResourcesHandler.load_map()

        map_file = pillow_to_file(map_image, "map.png")
        await ctx.reply(file=map_file)

    @command()
    @guild_only()
    @has_active_game()
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

        countries = [CountryModel(
                name=country.name,
                hex_color=country.color,
                tiles=[tile.code for tile in country.tiles],
            ) for country in countries]

        countries_image = ResourcesHandler.draw_countries(countries)
        countries_file = pillow_to_file(countries_image, "countries.png")
        await ctx.reply(file=countries_file)

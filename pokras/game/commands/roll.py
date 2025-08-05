from random import seed, randint

from discord.ext.commands import Cog, command, Context

from game.commands.checks import has_active_game
from game.queries.get_country import get_country_by_name
from game.queries.get_game import get_active_game_by_channel_id
from game.responses.country import CountryResponses
from game.responses.roll import RollResponses
from game.text.parser import CommentParser


def dices(seed_value: int, count: int = 5) -> list[int]:
    """
    Generates `count` number of random numbers between 0 and 9 based on provided seed.

    Args:
        seed_value: seed value
        count: number of random numbers to generate
    """
    seed(seed_value)
    return [randint(0, 9) for _ in range(count)]


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
            response += "ролл против"
            await ctx.reply(response)
            return

        if CommentParser.is_roll_on_neutral(prompt):
            response += "ролл на расширение"
            await ctx.reply(response)
            return

        tiles = CommentParser.process_tiles(prompt)
        response += f"\n({' '.join(tiles)})"

        await ctx.reply(response)

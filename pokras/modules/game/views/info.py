from discord.ext.commands import Cog, group, Context

from modules.game.queries.get_game import get_active_game_by_channel_id
from modules.game.service.service import parse_values
from utils.checks import has_active_game


class InfoGroup(Cog):
    @group()
    async def game(self, ctx: Context): ...

    @game.command()
    @has_active_game()
    async def info(self, ctx: Context):
        game = get_active_game_by_channel_id(ctx.channel.id)

        # todo: move to response
        response = []

        # map
        response.append(f"Карта: {game.map.name}")

        # cooldown
        if not game.use_cooldown:
            cd = "Кд: нет"
        elif game.cooldown < 60:
            cd = f"Кд: {game.cooldown}с"
        else:
            cd = f"Кд: {game.cooldown // 60}мин" + (f" {game.cooldown % 60}с" if game.cooldown % 60 else "")
        response.append(cd)

        # rolls
        v = parse_values(game.roll_values)
        response.append(v.dump_to_info_message())

        response = "\n".join(response)
        await ctx.send(response)

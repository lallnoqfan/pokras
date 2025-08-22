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
        cooldown_seconds = round(game.cooldown.total_seconds()) if game.cooldown is not None else 0
        if not game.use_cooldown:
            cd = "Кд: нет"
        elif cooldown_seconds < 60:
            cd = f"Кд: {cooldown_seconds}с"
        else:
            cd = f"Кд: {cooldown_seconds // 60}мин" + (f" {cooldown_seconds % 60}с" if cooldown_seconds % 60 else "")
        response.append(cd)

        # rolls
        v = parse_values(game.roll_values)
        response.append(v.dump_to_info_message())

        response = "\n".join(response)
        await ctx.send(response)

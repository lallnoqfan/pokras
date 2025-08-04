from discord.ext.commands import Context, check

from game.queries.get_game import get_active_game_by_channel_id
from game.responses.game import GameResponses


def is_admin():
    """
    Декоратор-чек, проверяющий, обладает ли вызвавший команду
    пользователь правами администратора сервера.
    """
    async def predicate(ctx: Context):
        if ctx.author.guild_permissions.administrator:
            return True

        if ctx.invoked_with == ctx.command.name:
            await ctx.send(f"Sorry, {ctx.author.mention}, you must be an administrator to use this command.")
        return False

    return check(predicate)


def has_active_game():
    """
    Декоратор-чек, проверяющий наличие активных игр в текущем канале.
    """
    async def predicate(ctx: Context):
        game = get_active_game_by_channel_id(ctx.channel.id)
        if game:
            return True

        if ctx.invoked_with == ctx.command.name:
            await ctx.send(GameResponses.no_active_games())
        return False

    return check(predicate)


def has_no_active_games():
    """
    Декоратор-чек, проверяющий отсутствие активных игр в текущем канале.
    """
    async def predicate(ctx: Context):
        game = get_active_game_by_channel_id(ctx.channel.id)
        if not game:
            return True

        if ctx.invoked_with == ctx.command.name:
            await ctx.send(GameResponses.active_game_already_exists(game))
        return False

    return check(predicate)

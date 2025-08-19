from discord.ext.commands import Converter, Context, BadArgument

from modules.game.service.models.roll_type import RollType


class RollTypeConverter(Converter):
    async def convert(self, ctx: Context, roll_type: str):
        try:
            return RollType[roll_type.lower()]
        except KeyError:
            pass

        for member in RollType:
            if member.value == roll_type:
                return member

        raise BadArgument(f"\"{roll_type}\" is not a valid roll type")

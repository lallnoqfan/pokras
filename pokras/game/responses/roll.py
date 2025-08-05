class RollResponses:

    # ========= MISSING ARGUMENTS =========

    @staticmethod
    def missing_prompt() -> str:
        return "prompt is required"

    # ========= FAILURE =========

    # ========= SUCCESS =========

    @staticmethod
    def roll(nums: list[int], roll_value: int) -> str:
        response = "`" + "` `".join(map(str, nums)) + "`"
        response += f" = {roll_value} tile{'s' if roll_value != 1 else ''}\n"
        return response

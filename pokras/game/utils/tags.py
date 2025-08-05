class Tags:
    @staticmethod
    def spoiler(text: str) -> str:
        return f"||{text}||"

    @staticmethod
    def bold(text: str) -> str:
        return f"**{text}**"

    @staticmethod
    def code(text: str) -> str:
        return f"`{text}`"

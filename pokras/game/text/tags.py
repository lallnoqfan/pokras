class Tags:
    @staticmethod
    def spoiler(text: str) -> str:
        return f"||{text}||"

    @classmethod
    def bold(cls, text: str) -> str:
        return f"**{text}**"

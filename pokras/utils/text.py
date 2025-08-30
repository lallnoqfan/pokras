from re import compile, search


class Tags:
    @staticmethod
    def spoiler(text: str) -> str:
        return f"||{text}||"

    @staticmethod
    def bold(text: str) -> str:
        return f"**{text}**"

    @staticmethod
    def italic(text: str) -> str:
        return f"*{text}*"

    @staticmethod
    def code(text: str) -> str:
        return f"`{text}`"


def cyrillic_to_roman(s: str) -> str:
    """
    Converts cyrillic letters to corresponding roman counterparts.
    """
    replace_table = {  # this dict is kinda incomplete
        'а': 'a',      # works fine with so called "classic" russian map
        'б': 'b',      # but it might require some adjustments for other maps
        'в': 'b',
        'с': 'c',
        'ц': 'c',
        'д': 'd',
        'е': 'e',
        'ф': 'f',
        'г': 'g',  # like here, for korea map
        'ж': 'g',
    }
    for cyrillic, roman in replace_table.items():
        s = s.replace(cyrillic, roman)
    return s


def parse_color(color_like: str) -> str | None:
    color_like = cyrillic_to_roman(color_like.strip().lower())
    pattern = compile(r"#?([a-f0-9]{6}|[a-f0-9]{3})")
    res = search(pattern, color_like)
    if not res:
        return None
    hex_code = res.group(1)
    if len(hex_code) == 3:
        hex_code = "".join(c * 2 for c in hex_code)
    return f"#{hex_code}"

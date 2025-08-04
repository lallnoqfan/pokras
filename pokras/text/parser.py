from re import compile, match, search, findall, IGNORECASE
from typing import List, Tuple


class CommentParser:
    @staticmethod
    def _cyrillic_to_roman(s: str) -> str:
        cyrillic = {
            'а': 'a',
            'б': 'b',
            'в': 'b',
            'с': 'c',
            'ц': 'c',
            'д': 'd',
            'е': 'e',
            'ф': 'f',
        }
        for key in cyrillic:
            s = s.replace(key, cyrillic[key])
        return s

    @classmethod
    def parse_roll_base(cls, comment: str) -> Tuple[str, str] | None:
        pattern = compile(
            r"(рол{1,10}база|rol{1,10}base)\s*?\n(.+?)\s*?\n#?([a-fA-F0-9]{6})",
            flags=IGNORECASE,
        )
        res = search(pattern, comment)
        if not res:
            return

        name = res.group(2)         # "(.+?)"
        color = f"#{res.group(3)}"  # "#?([a-fA-F0-9]{6})"
        color = cls._cyrillic_to_roman(color.lower())

        return name, color

    @classmethod
    def parse_roll(cls, comment: str) -> Tuple[int, List[str]] | None:
        pattern = compile(
            r"(^|\n)>>(\d+?)\s*\n[^\n]*?(rol|рол)[^\n]*?((\d+[a-zа-я]* ?)+)",
            flags=IGNORECASE,
        )
        res = search(pattern, comment)
        if not res:
            return

        num = res.group(2)    # >>(\d+?)
        tiles = res.group(4)  # ((\d+[a-zа-я]* ?)+)

        # tiles string processing

        tiles = tiles.lower()                   # "2B 3Ф" -> "2b 3ф"
        tiles = cls._cyrillic_to_roman(tiles)  # "2b 3ф" -> "2b 3f"
        tiles = tiles.split()                   # "2b 3f" -> ["2b", "3f"]

        # ["1a2b3cd"] -> ["1a", "2b", "3cd"]
        i = 0
        while i < len(tiles):
            res = findall(r"\d+[a-z]+", tiles[i])

            if len(res) <= 1:
                i += 1
                continue

            tiles.pop(i)
            for s in res:
                tiles.insert(i, s)
                i += 1

        # ["1abc"] -> ["1a", "1b", "1c"]
        i = 0
        while i < len(tiles):
            res = match(r"(\d+)([a-zA-Z]{2,})", tiles[i])

            if not res:
                i += 1
                continue

            tiles.pop(i)
            for s in [res.group(1) + c for c in res.group(2)]:
                tiles.insert(i, s)
                i += 1

        # duplicates clearing
        result = []
        [result.append(tile) for tile in tiles if tile not in result]

        return int(num), result

    @staticmethod
    def parse_roll_on_neutral(comment: str) -> int | None:
        pattern = compile(
            r"(\n|^)>>(\d+?)\s*\n[^\n]*?(rol|рол)[^\n]*?"
            r"(расширение|expan[ds])",
            flags=IGNORECASE
        )
        r = search(pattern, comment)
        if not r:
            return
        return int(r.group(2))

    @staticmethod
    def parse_roll_against(comment: str) -> Tuple[int, str] | None:
        pattern = compile(
            r"(\n|^)>>(\d+?)\s*\n[^\n]*?(rol|рол)[^\n]*?"
            r"(против|against) ([а-я ]{1,50})",
            flags=IGNORECASE
        )
        r = search(pattern, comment)
        if not r:
            return

        num = int(r.group(2))  # >>(\d+?)
        name = r.group(5)      # ([а-я ]{1,50})

        return num, name

    @staticmethod
    def get_roll_value(num: int | str) -> int:
        vals = {
            1: 0,
            2: 1,
            3: 3,
            4: 5,
            5: 8,
        }
        specials = {
            compile(r"^.*?((\d)\2(?!\2))((\d)(\4{2}))$"): 4,  # 11999 (2+3)
            compile(r"^.*?((\d)\2{2}(?!\2))((\d)(\4))$"): 4,  # 11199 (3+2)
            compile(r"^.*?((\d)\2(?!\2))((\d)(\4))$"):    2,  # 1199  (2+2)
        }

        num = str(num)
        for pattern in specials:
            if match(pattern, num):
                return specials[pattern]

        num = num[::-1]
        c = 1
        while c < len(num) and num[c - 1] == num[c]:
            c += 1
        val = vals.get(c, 0)
        return val

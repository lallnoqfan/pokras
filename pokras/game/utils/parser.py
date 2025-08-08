from re import compile, match, search, findall


class CommentParser:
    _against_keywords = ("против", "against")
    _expansion_keywords = ("расширение", "expand")

    @staticmethod
    def _cyrillic_to_roman(s: str) -> str:
        """
        Converts cyrillic letters to corresponding roman counterparts.
        """
        cyrillic_to_roman = {  # this dict is kinda incomplete
            'а': 'a',          # works fine with so called "classic" russian map
            'б': 'b',          # but it might require some adjustments for other maps
            'в': 'b',
            'с': 'c',
            'ц': 'c',
            'д': 'd',
            'е': 'e',
            'ф': 'f',
        }
        for cyrillic, roman in cyrillic_to_roman.items():
            s = s.replace(cyrillic, roman)
        return s

    @classmethod
    def parse_color(cls, color_like: str) -> str | None:
        # maybe should add some tests. todo?
        color_like = cls._cyrillic_to_roman(color_like.strip().lower())
        pattern = compile(r"#?([a-f0-9]{6}|[a-f0-9]{3})")
        res = search(pattern, color_like)
        if not res:
            return None
        hex_code = res.group(1)
        if len(hex_code) == 3:
            hex_code = "".join(c * 2 for c in hex_code)
        return f"#{hex_code}"

    @classmethod
    def process_tiles(cls, tiles: str) -> list[str]:
        """
        Tiles list normalization.
        """
        tiles = tiles.lower()                  # "2B 3Ф" -> "2b 3ф"
        tiles = cls._cyrillic_to_roman(tiles)  # "2b 3ф" -> "2b 3f"
        tiles = tiles.split()                  # "2b 3f" -> ["2b", "3f"]

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
        tiles = list(set(tiles))
        tiles.sort()
        # todo: it would be great if we could preserve initial order of tiles tiles as it is in user's input
        #       for now, after parsing, initial order is totally lost, so should probably be fixed

        return tiles

    @staticmethod
    def get_roll_value(num: int | str) -> int:
        vals = {
            1: 1,   # normal roll
            2: 3,   # double
            3: 5,   # triple
            4: 9,   # quadruple
            5: 15,  # quintuple
        }
        specials = {
            compile(r"^.*?((\d)\2(?!\2)(\d)\3\3)$"):   7,  # 11999 double-triple
            compile(r"^.*?((\d)\2\2(?!\2)(\d)\3)$"):   7,  # 11199 triple-double
            compile(r"^.*?((\d)\2(?!\2)(\d)\3)$"):     4,  # 1199  double-double
            compile(r"^.*?((\d)(?!\2)\d\2)$"):         1,  # 191   3d pali
            compile(r"^.*?((\d)(?!\2)(\d)\3\2)$"):     3,  # 1991  4d pali
            compile(r"^.*?((\d)(?!\2\2)(\d)\d\3\2)$"): 5,  # 19191 5d pali
            # todo: add straights?
            #       then make it possible to adjust values in runtime
        }

        result_roll_value = 0

        num = str(num)
        for pattern in specials:
            if match(pattern, num):
                result_roll_value = max(result_roll_value, specials[pattern])

        num = num[::-1]
        c = 1
        while c < len(num) and num[c - 1] == num[c]:
            c += 1
        result_roll_value = max(result_roll_value, vals.get(c, 0))

        return result_roll_value

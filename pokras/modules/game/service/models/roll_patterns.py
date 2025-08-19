from enum import Enum
from re import compile


class RollPatterns(Enum):
    one           = compile(r"^.*?(1)$")                                                                # noqa: E221
    two           = compile(r"^.*?(2)$")                                                                # noqa: E221
    three         = compile(r"^.*?(3)$")                                                                # noqa: E221
    four          = compile(r"^.*?(4)$")                                                                # noqa: E221
    five          = compile(r"^.*?(5)$")                                                                # noqa: E221
    six           = compile(r"^.*?(6)$")                                                                # noqa: E221
    seven         = compile(r"^.*?(7)$")                                                                # noqa: E221
    eight         = compile(r"^.*?(8)$")                                                                # noqa: E221
    nine          = compile(r"^.*?(9)$")                                                                # noqa: E221
    zero          = compile(r"^.*?(0)$")                                                                # noqa: E221

    double        = compile(r"^.*?((\d)\2)$")                                                           # noqa: E221
    triple        = compile(r"^.*?((\d)\2{2})$")                                                        # noqa: E221
    quadruple     = compile(r"^.*?((\d)\2{3})$")                                                        # noqa: E221
    quintuple     = compile(r"^.*?((\d)\2{4,})$")                                                       # noqa: E221

    double_double = compile(r"^.*?((\d)\2(?!\2)(\d)\3)$")                                               # noqa: E221
    double_triple = compile(r"^.*?((\d)\2(?!\2)(\d)\3\3)$")                                             # noqa: E221
    triple_double = compile(r"^.*?((\d)\2\2(?!\2)(\d)\3)$")                                             # noqa: E221

    pali3d        = compile(r"^.*?((\d)(?!\2)\d\2)$")                                                   # noqa: E221
    pali4d        = compile(r"^.*?((\d)(?!\2)(\d)\3\2)$")                                               # noqa: E221
    pali5d        = compile(r"^.*?((\d)(?!\2\2)(\d)\d\3\2)$")                                           # noqa: E221

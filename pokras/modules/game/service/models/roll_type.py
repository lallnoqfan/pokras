from enum import Enum


class RollType(Enum):
    # todo: add straights?
    one   = "1"                                                                                         # noqa: E221
    two   = "2"                                                                                         # noqa: E221
    three = "3"                                                                                         # noqa: E221
    four  = "4"                                                                                         # noqa: E221
    five  = "5"                                                                                         # noqa: E221
    six   = "6"                                                                                         # noqa: E221
    seven = "7"                                                                                         # noqa: E221
    eight = "8"                                                                                         # noqa: E221
    nine  = "9"                                                                                         # noqa: E221
    zero  = "0"                                                                                         # noqa: E221

    double    = "Дабл"                                                                                  # noqa: E221
    triple    = "Трипл"                                                                                 # noqa: E221
    quadruple = "Квадрипл"                                                                              # noqa: E221
    quintuple = "Пентипл"                                                                               # noqa: E221

    double_double = "Даблодабл"                                                                         # noqa: E221
    double_triple = "Даблотрипл"                                                                        # noqa: E221
    triple_double = "Триплодабл"                                                                        # noqa: E221

    pali3d = "3д пали"                                                                                  # noqa: E221
    pali4d = "4д пали"                                                                                  # noqa: E221
    pali5d = "5д пали"                                                                                  # noqa: E221

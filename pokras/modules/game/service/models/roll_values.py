from dataclasses import dataclass

from modules.game.service.models.roll_type import RollType


@dataclass
class RollValues:
    one:   int = 1
    two:   int = 1
    three: int = 1
    four:  int = 1
    five:  int = 1
    six:   int = 1
    seven: int = 1
    eight: int = 1
    nine:  int = 1
    zero:  int = 1

    double:    int = 3
    triple:    int = 5
    quadruple: int = 9
    quintuple: int = 15

    double_double: int = 4
    double_triple: int = 7
    triple_double: int = 7

    pali3d: int = 2
    pali4d: int = 3
    pali5d: int = 5

    @classmethod
    def from_list(cls, values: list[int]):
        field_names = list(cls.__annotations__.keys())
        if not len(values) == len(field_names):
            raise ValueError(f"Wrong number of values, expected {len(field_names)}, got {len(values)}")
        data = {field: value for field, value in zip(field_names, values)}
        return cls(**data)

    def dump_to_info_message(self):
        number_fields = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "zero"]
        result = ["Роллы:"]

        value = getattr(self, number_fields[0])
        all_same = all(getattr(self, name) == value for name in number_fields)

        if all_same:
            if value != 0:
                result.append(f"- Цифры: {value}т")
        else:
            number_bins: dict[int, list[str]] = {}

            for name in number_fields:
                value = getattr(self, name)
                if value not in number_bins:
                    number_bins[value] = []
                number_bins[value].append(name)

            sorted_bins = number_bins.keys()
            for value in sorted_bins:
                names_in_bin = number_bins[value]
                display_values = sorted([RollType[name].value for name in names_in_bin])
                joined_names = ", ".join(display_values)
                result.append(f"- {joined_names}: {value}т")

        other_fields = [
            "double", "triple", "quadruple", "quintuple",
            "double_double", "double_triple", "triple_double",
            "pali3d", "pali4d", "pali5d"
        ]
        for name in other_fields:
            value = getattr(self, name)
            if value:
                result.append(f"- {RollType[name].value}: {value}т")

        return "\n".join(result)

    def dump_to_string(self) -> str:
        return ",".join(map(str, [getattr(self, name) for name in self.__annotations__.keys()]))

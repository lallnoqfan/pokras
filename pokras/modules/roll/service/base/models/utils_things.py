from dataclasses import dataclass
from pathlib import Path


@dataclass
class Layer:
    file_path: Path
    paste_bias: tuple[int, int] = (0, 0)

    def __hash__(self) -> int:
        return hash(self.file_path)

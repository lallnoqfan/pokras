from json import load
from pathlib import Path

from memory_profiler import profile

from config import Paths
from utils.perf import time_performance


@time_performance
@profile
def load_jsons(jsons: list[Path]):
    data = []
    for path in jsons:
        with open(path, "r", encoding="utf-8") as f:
            data.append(load(f))


if __name__ == '__main__':
    paths = [
        Paths.EU_CLASSIC_TILES,
        Paths.KOREA_TILES,
        Paths.OPS_ASS_TILES,
        Paths.STALKER_TILES,
    ]
    load_jsons(paths)

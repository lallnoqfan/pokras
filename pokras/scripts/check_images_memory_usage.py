from pathlib import Path

from memory_profiler import profile
from PIL import Image

from config import Paths
from utils.perf import function_performance


@function_performance
@profile
def load_images(rgb_layers: list[Path], rgba_layers: list[Path]):
    images = []
    for path in rgb_layers:
        images.append(Image.open(path).convert("RGB"))
    for path in rgba_layers:
        images.append(Image.open(path).convert("RGBA"))


if __name__ == '__main__':
    rgb = [
        Paths.EU_CLASSIC_MAP,
        Paths.KOREA_MAP,
        Paths.STALKER_MAP,
    ]
    rgba = [
        Paths.OPS_ASS / "tiles_ids.png",
        Paths.OPS_ASS / "tiles_map.png",
        Paths.OPS_ASS / "bg_rachnera.png",
    ]
    load_images(rgb, rgba)

from memory_profiler import profile
from PIL import Image

from config import Paths


@profile
def load_image_and_process():
    img = Image.open(Paths.OPS_ASS / "bg_rachnera.png").convert("RGBA")
    image = img.copy()
    image2 = img.copy()
    return img


if __name__ == '__main__':
    load_image_and_process()

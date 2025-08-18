from io import BytesIO

from PIL.Image import Image
from discord import File


def pillow_to_file(pillow_image: Image, file_name: str, file_format: str = 'PNG') -> File:
    with BytesIO() as binary_image:
        pillow_image.save(binary_image, file_format)
        binary_image.seek(0)
        discord_file = File(fp=binary_image, filename=file_name)
    return discord_file

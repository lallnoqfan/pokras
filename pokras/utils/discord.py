from io import BytesIO

import cv2
import numpy as np
from PIL.Image import Image
from discord import File

from utils.perf import function_performance


@function_performance
def pillow_to_file(pillow_image: Image, file_name: str, file_format: str = 'PNG') -> File:
    with BytesIO() as binary_image:
        pillow_image.save(binary_image, file_format)
        binary_image.seek(0)
        discord_file = File(fp=binary_image, filename=file_name)
    return discord_file


@function_performance
def cv2_to_file(cv2_image: np.ndarray, file_name: str, file_format: str = 'PNG') -> File:
    """
    Converts an OpenCV image (NumPy array) directly to a Discord File.
    """
    extension = f'.{file_format.lower()}'
    success, buffer = cv2.imencode(extension, cv2_image)

    if not success:
        raise ValueError("Could not encode image to specified format.")

    binary_image = BytesIO(buffer)
    binary_image.seek(0)

    discord_file = File(fp=binary_image, filename=file_name)
    return discord_file

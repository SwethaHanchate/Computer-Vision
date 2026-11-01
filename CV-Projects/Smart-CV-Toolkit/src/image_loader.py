import cv2
from pathlib import Path


def load_image(image_path):
    """
    Load an image from given file path.
    image_path : path to the input image.
    Returns: loaded image as a NumPy array.
    """
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    if not image_path.is_file():
        raise ValueError(f"Path is not a file: {image_path}")
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Unable to load image: {image_path}")
    return image

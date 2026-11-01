import cv2
from src.validation import validate_image_path, validate_image_data, validate_image_dimensions


def load_image(image_path):
    """
    Load an image from given file path.
    image_path : path to the input image.
    Returns: loaded image as a NumPy array.
    """
    validate_image_path(image_path)

    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError(f"Unable to load image: {image_path}")

    validate_image_data(image)
    validate_image_dimensions(image)

    return image

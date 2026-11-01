import cv2
from pathlib import Path


def save_image(image, output_path):
    """
    Saved image to specified path.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    success = cv2.imwrite(str(output_path), image)

    if not success:
        raise ValueError(f"Unavle to save image: {output_path}")

    return output_path

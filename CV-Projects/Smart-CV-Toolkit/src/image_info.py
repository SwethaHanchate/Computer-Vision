from pathlib import Path


def get_image_info(image, image_path):
    """
    Extract basic information about an image.
    """

    height, width = image.shape[:2]
    channels = 1 if image.ndim == 2 else image.shape[2]

    image_path = Path(image_path)

    file_size = image_path.stat().st_size
    file_size_kb = file_size / 1024

    return {
        "width": width,
        "height": height,
        "channels": channels,
        "shape": image.shape,
        "dtype": str(image.dtype),
        "file_size_kb": round(file_size_kb, 2),
    }

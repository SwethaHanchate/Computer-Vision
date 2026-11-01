from pathlib import Path
import numpy as np


def validate_image_path(image_path):
    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    if not image_path.is_file():
        raise ValueError(f"Path is not a file: {image_path}")

    allowed_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]

    if image_path.suffix.lower() not in allowed_extensions:
        raise ValueError(f"Unsupported image format: {image_path.suffix}")

    return True


def validate_image_data(image):
    if image is None:
        raise ValueError("Image data is empty.")

    if not isinstance(image, np.ndarray):
        raise TypeError("Image must be a NumPy array.")

    if image.size == 0:
        raise ValueError("Image contains no pixel data.")

    if image.ndim not in (2, 3):
        raise ValueError("Invalid image dimensions.")

    if image.ndim == 3 and image.shape[2] not in (1, 3, 4):
        raise ValueError("Invalid number of image channels.")

    return True


def validate_image_dimensions(image, min_width=1, min_height=1):
    height, width = image.shape[:2]

    if width < min_width or height < min_height:
        raise ValueError("Image dimensions are too small.")

    return True


def validate_video_path(video_path):
    video_path = Path(video_path)

    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    if not video_path.is_file():
        raise ValueError(f"Path is not a file: {video_path}")

    allowed_extensions = [".mp4", ".avi", ".mov", ".mkv"]

    if video_path.suffix.lower() not in allowed_extensions:
        raise ValueError(f"Unsupported video format: {video_path.suffix}")

    return True


def validate_frame_data(frame):
    return validate_image_data(frame)


def validate_video_info(video_info):
    if video_info["width"] <= 0:
        raise ValueError("Invalid video width.")

    if video_info["height"] <= 0:
        raise ValueError("Invalid video height.")

    if video_info["fps"] <= 0:
        raise ValueError("Invalid video FPS.")

    if video_info["total_frames"] <= 0:
        raise ValueError("Invalid video frame count.")

    return True

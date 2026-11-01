import cv2


def resize_image(image, width=None, height=None):
    """
    Changes image dimensions while preserving the aspect ratio
    when only one dimension is provided.
    """
    if width is None and height is None:
        raise ValueError("Provide width or height.")

    original_height, original_width = image.shape[:2]

    if width is None:
        ratio = height / original_height
        width = int(original_width * ratio)

    elif height is None:
        ratio = width / original_width
        height = int(original_height * ratio)

    resized = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

    return resized


def crop_image(image, x, y, width, height):
    """
    Extract a specific region from an image.
    """
    image_height, image_width = image.shape[:2]

    if x < 0 or y < 0:
        raise ValueError("Crop coordinates cannot be negative.")

    if width <= 0 or height <= 0:
        raise ValueError("Crop dimensions must be positive.")

    if x + width > image_width or y + height > image_height:
        raise ValueError("Crop region exceeds image boundaries.")

    cropped = image[y : y + height, x : x + width]

    return cropped

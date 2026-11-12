import cv2
import numpy as np


def adjust_brightness(image, beta):
    """Increase or decrease brightness using an additive offset."""
    result = image.astype(np.float32) + beta
    return np.clip(result, 0, 255).astype(np.uint8)


def adjust_contrast(image, alpha):
    """Adjust contrast using a multiplicative factor."""
    result = image.astype(np.float32) * alpha
    return np.clip(result, 0, 255).astype(np.uint8)


def apply_gamma_correction(image, gamma):
    """Gamma < 1 brightens; gamma > 1 darkens."""
    if gamma <= 0:
        raise ValueError("Gamma must be greater than zero.")

    normalized = image.astype(np.float32) / 255.0
    corrected = np.power(normalized, gamma)

    return np.clip(corrected * 255, 0, 255).astype(np.uint8)


def apply_negative(image):
    """Invert image intensity values."""
    return 255 - image


def apply_log_transformation(image):
    """Enhance darker intensity regions using logarithmic transformation."""
    image_float = image.astype(np.float32)
    max_value = np.max(image_float)

    if max_value == 0:
        return image.copy()

    c = 255 / np.log1p(max_value)
    transformed = c * np.log1p(image_float)

    return np.clip(transformed, 0, 255).astype(np.uint8)


def apply_contrast_stretching(image):
    """Expand image intensity range from its minimum to maximum."""
    min_value = np.min(image)
    max_value = np.max(image)

    if min_value == max_value:
        return image.copy()

    image_float = image.astype(np.float32)

    stretched = (image_float - min_value) * 255.0 / (max_value - min_value)

    return np.clip(stretched, 0, 255).astype(np.uint8)


def apply_histogram_equalization(image):
    """Apply histogram equalization to a grayscale image."""
    if image.ndim != 2:
        raise ValueError("Histogram equalization requires a grayscale image.")

    return cv2.equalizeHist(image)


def apply_clahe(image, clip_limit=2.0, tile_grid_size=(8, 8)):
    """Apply CLAHE to a grayscale image."""
    if image.ndim != 2:
        raise ValueError("CLAHE requires a grayscale image.")

    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)

    return clahe.apply(image)

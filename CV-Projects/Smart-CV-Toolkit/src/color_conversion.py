import cv2


def convert_to_rgb(image):
    """
    Convert to RGB color space.
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def convert_to_grayscale(image):
    """
    Convert to grayscale color space.
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def convert_to_hsv(image):
    """
    Convert to Hue Saturation Value HSV color space.
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


def convert_to_lab(image):
    """
    Convert to CIE Lab color space.
    Lab is a perceptually oriented color space that separates lightness from two color opponent components.
    L* : Lightness
    a* : Green to Red
    b* : Blue to Yellow
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

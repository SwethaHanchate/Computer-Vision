import cv2
import numpy as np
import matplotlib.pyplot as plt


def create_grayscale_histogram(image):
    """
    Generate histogram for grayscale image.
    """
    if image.ndim == 3:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image

    histogram = cv2.calcHist([gray_image], [0], None, [256], [0, 256])

    fig, ax = plt.subplots(figsize=(7, 3))

    ax.plot(histogram, color="black")
    ax.set_title("Grayscale Histogram")
    ax.set_xlabel("Pixel Intensity")
    ax.set_ylabel("Pixel Count")
    ax.set_xlim([0, 256])
    ax.grid(alpha=0.3)

    fig.tight_layout()
    return fig


def create_rgb_histogram(image):
    """
    Generate separate Red, Green and Blue histograms.
    """
    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError("RGB histogra, requires a 3-channel color image.")

    fig, ax = plt.subplots(figsize=(7, 3))
    channels = [(2, "Red", "red"), (1, "Green", "green"), (0, "Blue", "blue")]

    for channel_index, channel_name, color in channels:
        histogram = cv2.calcHist([image], [channel_index], None, [256], [0, 256])

        ax.plot(histogram, color=color, label=channel_name)

    ax.set_title("RGB Histogram")
    ax.set_xlabel("Pixel Intensity")
    ax.set_ylabel("Pixel Count")
    ax.set_xlim([0, 256])
    ax.legend()
    ax.grid(alpha=0.3)

    fig.tight_layout()

    return fig

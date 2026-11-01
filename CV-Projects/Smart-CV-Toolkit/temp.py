from src.image_loader import load_image
from src.transformations import resize_image, crop_image, flip_image, rotate_image, translate_image
import cv2
from src.color_conversion import (
    convert_to_rgb,
    convert_to_grayscale,
    convert_to_hsv,
    convert_to_lab,
)

image = load_image("data/input/sample.jpeg")

resized = resize_image(image, width=500)
cropped = crop_image(image, 100, 100, 400, 500)
flipped = flip_image(image, "horizontal")
rotated = rotate_image(image, 45)
translated = translate_image(image, 100, 50)

# print("Original:", image.shape)
# print("Resized:", resized.shape)
# print("Cropped:", cropped.shape)
# print("Flipped:", flipped.shape)
# print("Rotated:", rotated.shape)
# print("Translated:", translated.shape)

from src.color_conversion import (
    convert_to_rgb,
    convert_to_grayscale,
    convert_to_hsv,
    convert_to_lab,
)

rgb = convert_to_rgb(image)
gray = convert_to_grayscale(image)
hsv = convert_to_hsv(image)
lab = convert_to_lab(image)

print("Original:", image.shape)
print("RGB:", rgb.shape)
print("Grayscale:", gray.shape)
print("HSV:", hsv.shape)
print("Lab:", lab.shape)


# cv2.imshow("Lab", lab_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

from src.image_loader import load_image
from src.transformations import resize_image, crop_image, flip_image, rotate_image, translate_image

image = load_image("data/input/sample.jpeg")

resized = resize_image(image, width=500)
cropped = crop_image(image, 100, 100, 400, 500)
flipped = flip_image(image, "horizontal")
rotated = rotate_image(image, 45)
translated = translate_image(image, 100, 50)

print("Original:", image.shape)
print("Resized:", resized.shape)
print("Cropped:", cropped.shape)
print("Flipped:", flipped.shape)
print("Rotated:", rotated.shape)
print("Translated:", translated.shape)

from src.image_loader import load_image
from src.transformations import resize_image, crop_image, flip_image, rotate_image, translate_image
import cv2

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

# print("Original:", image.shape)
# print("RGB:", rgb.shape)
# print("Grayscale:", gray.shape)
# print("HSV:", hsv.shape)
# print("Lab:", lab.shape)


from src.annotations import draw_line, draw_rectangle, draw_circle, draw_ellipse, add_text

annotated = draw_line(image, (50, 50), (600, 300))

annotated = draw_rectangle(annotated, (100, 350), (500, 900))

annotated = draw_circle(annotated, (550, 600), 80)

annotated = draw_ellipse(annotated, (350, 1100), (150, 70), angle=30)

annotated = add_text(annotated, "Computer Vision", (100, 1200), font_scale=1.5)

cv2.imwrite("data/output/all_annotations.jpg", annotated)

print("Original:", image.shape)
print("Final annotated:", annotated.shape)
print("All annotations completed!")


# cv2.imshow("Annotated", text)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

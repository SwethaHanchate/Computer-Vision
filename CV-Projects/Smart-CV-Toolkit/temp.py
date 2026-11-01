from src.image_loader import load_image
from src.image_info import get_image_info
from src.transformations import resize_image, crop_image, flip_image

image_path = "data/input/sample.jpeg"
image = load_image(image_path)

resized = resize_image(image, width=500)

cropped = crop_image(image, x=100, y=100, width=400, height=500)

flipped = flip_image(image, "horizontal")

print("Original: ", image.shape)
print("Flipped: ", flipped.shape)


# info = get_image_info(image, image_path)


# print("Image loaded successfully!")
# print("Image Information")
# for key, value in info.items():
#     print(f"{key}: {value}")

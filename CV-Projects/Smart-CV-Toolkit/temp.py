from src.image_loader import load_image
from src.image_info import get_image_info

image_path = "data/input/sample.jpeg"
image = load_image(image_path)

info = get_image_info(image, image_path)


print("Image loaded successfully!")
print("Image Information")
for key, value in info.items():
    print(f"{key}: {value}")

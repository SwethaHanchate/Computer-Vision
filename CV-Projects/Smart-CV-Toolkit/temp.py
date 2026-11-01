from src.image_loader import load_image

image = load_image("data/input/sample.jpeg")

print("Image loaded successfully!")
print("Image shape:", image.shape)
print("Image dtype:", image.dtype)

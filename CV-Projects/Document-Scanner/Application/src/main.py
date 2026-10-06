import cv2
import numpy as np
import matplotlib
from PIL import Image


image = cv2.imread("/Users/swethahanchate/Documents/Swetha/Work/Computer Vision/Practical/Computer-Vision/CV-Projects/Document-Scanner/Application/data/input/document.png")
if image is None:
    raise FileNotFoundError("Could not load the image")

print("Image loaded successfully")
print("Image shape: ", image.shape)


def resize_image(image, target_width=1000):
    height, width = image.shape[:2]
    scale = target_width / width

    new_width = int(width * scale)
    new_height = int(height * scale)

    resized = cv2.resize(image, (new_width, new_height), interpolation = cv2.INTER_AREA)
    return resized


"""Step 1: Resize th image."""
resized = resize_image(image)
print("Resized Shape: ", resized.shape)


"""Step 2: Convert the resized image to Grayscale."""
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
print("Grayscale Shape: ", gray.shape)


"""Step 3: Implement Gaussian Blur to reduce noise for Edge Detection."""
blurred = cv2.GaussianBlur(gray, (5,5), 0)
print("Blurred Shape: ", blurred.shape)


"""Step 4: Detect edges."""
edges = cv2.Canny(blurred, 50, 150)
print("Edges Shape: ", edges.shape)


"""Step 5: Find Contours."""
contours, hirearchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print("Number of Contours: ", len(contours))

# Contour area
for contour in contours:
    area = cv2.contourArea(contour)
    print(area)

# Sort contours
contours = sorted(contours, key=cv2.contourArea, reverse=True)
for i, contour in enumerate(contours[:10]):
    area = cv2.contourArea(contour)
    print(f"Contour {i}: Area = {area}")

# Visualize the contours
contour_image = resized.copy()
cv2.drawContours(contour_image, contours, -1, (0,255,0), 2)



# cv2.imshow("Original", image)
# cv2.imshow("Resized", resized)
# cv2.imshow("Grayscale", gray)
# cv2.imshow("Blurred", blurred)
cv2.imshow("Edges", edges)
cv2.imshow("Contours", contour_image)
cv2.waitKey(0)
cv2.destroyAllWindows()



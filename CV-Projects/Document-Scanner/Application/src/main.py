import cv2
import numpy as np
import matplotlib
from PIL import Image


image = cv2.imread("/Users/swethahanchate/Documents/Swetha/Work/Computer Vision/Practical/Computer-Vision/CV-Projects/Document-Scanner/Application/data/input/document2.png")
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

# Largest contour
document_contour = contours[0]

# Calculate Contour perimeter
perimeter = cv2.arcLength(document_contour, True)
print("Contouor Perimeter: ", perimeter)

# Approximate contour with polygon
epsilon = 0.02 * perimeter
approx = cv2.approxPolyDP(document_contour, epsilon, True)
print("Number of approximated points: ", len(approx))

# Visualize the contours
polygon_image = resized.copy()
cv2.drawContours(polygon_image, [approx], -1, (0,255,0), 3)

# Extract document corners
print("Document Corners:")
print(approx)
print("Approx Shape: ", approx.shape)

points = approx.reshape(4, 2)
print(points)

corner_image = resized.copy()
for i, point in enumerate(points):
    x, y = point
    cv2.circle(corner_image, (x, y), 10, (0,0,255), -1)
    cv2.putText(corner_image, str(i), (x+10, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
    

"""Step 6: Order the points."""
def order_points(points):

    points = np.asarray(points, dtype=np.float32)

    ordered = np.zeros((4, 2), dtype=np.float32)

    # Calculate x + y
    sums = points.sum(axis=1)

    # Calculate x - y
    differences = points[:, 0] - points[:, 1]

    # Top-left has the smallest x + y
    ordered[0] = points[np.argmin(sums)]

    # Bottom-right has the largest x + y
    ordered[2] = points[np.argmax(sums)]

    # Top-right has the largest x - y
    ordered[1] = points[np.argmax(differences)]

    # Bottom-left has the smallest x - y
    ordered[3] = points[np.argmin(differences)]

    return ordered

points = approx.reshape(4,2)
ordered_points = order_points(points)
print("Ordered Points: ")
print(ordered_points)






"""Step 7: Perspective Transformation."""
# Calculate document width
width_top = np.linalg.norm(ordered_points[1] - ordered_points[0])
width_bottom = np.linalg.norm(ordered_points[2] - ordered_points[3])
max_width = int(max(width_top, width_bottom))

# Calculate document hight
height_left = np.linalg.norm(ordered_points[3] - ordered_points[0])
height_right = np.linalg.norm(ordered_points[2] - ordered_points[1])
max_height = int(max(height_left, height_right))

# Calculate destination points
destination_points = np.array([[0,0], [max_width-1, 0], [max_width-1, max_height-1], [0, max_height-1]], dtype=np.float32)

# Calculate prspective transformation matrix
matrix = cv2.getPerspectiveTransform(ordered_points, destination_points)

# Apply perspective transformation
wraped = cv2.warpPerspective(resized, matrix, (max_width, max_height))
print("Wraped shape: ", wraped.shape)



# cv2.imshow("Original", image)
# cv2.imshow("Resized", resized)
# cv2.imshow("Grayscale", gray)
# cv2.imshow("Blurred", blurred)
# cv2.imshow("Edges", edges)
# cv2.imshow("Contours", contour_image)
# cv2.imshow("Approximated Document", polygon_image)
# cv2.imshow("Detected Corners", corner_image)
cv2.imshow("Original", resized)
cv2.imshow("Scanned Document", wraped)
cv2.waitKey(0)
cv2.destroyAllWindows()



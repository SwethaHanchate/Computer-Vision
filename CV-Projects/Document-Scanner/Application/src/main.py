import cv2
import numpy as np

# ==============================================================
# Configuration
# ==============================================================

INPUT_IMAGE_PATH = "/Users/swethahanchate/Documents/Swetha/Work/Computer Vision/Practical/Computer-Vision/CV-Projects/Document-Scanner/Application/data/input/document.png"
TARGET_WIDTH = 1000


# ==============================================================
# Image Processing Functions
# ==============================================================


def load_image(image_path):
    """Load an image from the given file path."""
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not load the image: {image_path}")
    return image


def resize_image(image, target_width=1000):
    """Resize the image while preserving aspect ratio."""
    height, width = image.shape[:2]
    scale = target_width / width
    new_width = int(width * scale)
    new_height = int(height * scale)
    resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    return resized


def order_points(points):
    """Order four points as TL, TR, BR, BL."""
    points = np.asarray(points, dtype=np.float32)
    ordered = np.zeros((4, 2), dtype=np.float32)

    sums = points.sum(axis=1)
    differences = points[:, 0] - points[:, 1]

    # Top-left
    ordered[0] = points[np.argmin(sums)]
    # Top-right
    ordered[1] = points[np.argmax(differences)]
    # Bottom-right
    ordered[2] = points[np.argmax(sums)]
    # Bottom-left
    ordered[3] = points[np.argmin(differences)]

    return ordered


def detect_document_corners(image):
    """Detect the four corners of the document."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        epsilon = 0.02 * perimeter
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) == 4:
            points = approx.reshape(4, 2)
            return order_points(points)
    raise ValueError("Could not detect a four-corner document.")


def perspective_transform(image, corners):
    """Apply perspective correction to the document."""
    top_left, top_right, bottom_right, bottom_left = corners

    width_top = np.linalg.norm(top_right - top_left)

    width_bottom = np.linalg.norm(bottom_right - bottom_left)

    max_width = int(max(width_top, width_bottom))

    height_left = np.linalg.norm(bottom_left - top_left)

    height_right = np.linalg.norm(bottom_right - top_right)

    max_height = int(max(height_left, height_right))

    destination_points = np.array(
        [[0, 0], [max_width - 1, 0], [max_width - 1, max_height - 1], [0, max_height - 1]],
        dtype=np.float32,
    )

    matrix = cv2.getPerspectiveTransform(corners, destination_points)

    warped = cv2.warpPerspective(image, matrix, (max_width, max_height))

    return warped


# ==============================================================
# Main Pipeline
# ==============================================================


def main():
    """Load Image"""
    image = load_image(INPUT_IMAGE_PATH)

    """Resize Image"""
    resized = resize_image(image, TARGET_WIDTH)
    print("Resized shape:", resized.shape)

    """Detect Document"""
    corners = detect_document_corners(resized)
    print("Detected document corners:")
    print(corners)

    """Perspective Correction"""
    wraped = perspective_transform(resized, corners)
    print("Wraped shape:", wraped.shape)

    """Display Results"""
    cv2.imshow("Original", resized)
    cv2.imshow("Scanned Document", wraped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ==============================================================
# Entry Point
# ==============================================================

if __name__ == "__main__":
    main()

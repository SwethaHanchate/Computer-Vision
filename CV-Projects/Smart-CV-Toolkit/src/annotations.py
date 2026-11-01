import cv2


def draw_line(image, start_point, end_point, color=(0, 0, 255), thickness=2):
    """
    Draws a straight line btw 2 points on an image.
    """
    annotated_image = image.copy()
    cv2.line(annotated_image, start_point, end_point, color, thickness)
    return annotated_image


def draw_rectangle(image, start_point, end_point, color=(0, 0, 255), thickness=2):
    """
    Draws a rectangular boundary around the selected region on an image.
    """
    annotated_image = image.copy()
    cv2.rectangle(annotated_image, start_point, end_point, color, thickness)
    return annotated_image


def draw_circle(image, center, radius, color=(255, 0, 0), thickness=2):
    """
    Draws a circle at a specified center point with a given radius.
    """
    annotated_image = image.copy()
    cv2.circle(annotated_image, center, radius, color, thickness)
    return annotated_image


def draw_ellipse(image, center, axes, angle=0, color=(0, 255, 255), thickness=2):
    """
    Draws an oval or elliptical shape on an image.
    """
    annotated_image = image.copy()
    cv2.ellipse(annotated_image, center, axes, angle, 0, 360, color, thickness)
    return annotated_image


def add_text(image, text, position, font_scale=1, color=(0, 255, 0), thickness=2):
    """
    Adds text or labels at a specified position on an image.
    """
    annotated_image = image.copy()
    cv2.putText(
        annotated_image,
        text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        color,
        thickness,
        cv2.LINE_AA,
    )
    return annotated_image

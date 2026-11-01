import cv2
from pathlib import Path
from src.validation import validate_video_path, validate_frame_data, validate_video_info


def open_video(video_path):
    """
    Open a video at given path and validate access to it.
    """
    validate_video_path(video_path)

    capture = cv2.VideoCapture(str(video_path))

    if not capture.isOpened():
        raise ValueError(f"Unable to open video: {video_path}")

    return capture


def read_frame(capture):
    """
    Extract frame from the video.
    """
    success, frame = capture.read()

    if not success:
        return None

    validate_frame_data(frame)

    return frame


def get_video_info(capture):
    """
    Extracts video properties like
    frame dimensions,
    frames per second and
    number of frames in the video.
    """
    video_info = {
        "width": int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "fps": int(capture.get(cv2.CAP_PROP_FPS)),
        "total_frames": int(capture.get(cv2.CAP_PROP_FRAME_COUNT)),
    }

    validate_video_info(video_info)

    return video_info


def extract_frames(capture):
    """
    Reads every frame until the video ends.
    """
    frames = []

    while True:
        success, frame = capture.read()

        if not success:
            break

        frames.append(frame)

    return frames


def save_video_frames(capture, output_dir, interval=30):
    """
    Saving selected frames as individual images.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    frame_count = 0
    saved_count = 0

    while True:
        success, frame = capture.read()

        if not success:
            break

        if frame_count % interval == 0:
            output_path = output_dir / f"frame_{frame_count}.jpg"
            if cv2.imwrite(str(output_path), frame):
                saved_count += 1

        frame_count += 1

    return saved_count


def process_video_frames(capture):
    """
    Process each frame individually without storing entire video in memory.
    """
    processed_count = 0

    while True:
        success, frame = capture.read()

        if not success:
            break

        # Convert each frame to grayscale
        processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        processed_count += 1

    return processed_count


def process_and_save_video(capture, output_path):
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = capture.get(cv2.CAP_PROP_FPS)

    output_path = Path(output_path).with_suffix(".mp4")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # H.264 codec
    fourcc = cv2.VideoWriter_fourcc(*"avc1")

    writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height), isColor=True)

    if not writer.isOpened():
        raise ValueError("H.264 encoding is unavailable in this OpenCV installation.")

    processed_count = 0

    try:
        while True:
            success, frame = capture.read()

            if not success:
                break

            # Convert frame to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Convert grayscale to 3-channel BGR
            output_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)

            writer.write(output_frame)
            processed_count += 1

    finally:
        writer.release()

    return processed_count

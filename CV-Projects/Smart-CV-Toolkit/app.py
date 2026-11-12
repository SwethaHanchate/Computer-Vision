import cv2
import numpy as np
import streamlit as st
from pathlib import Path
from src.image_info import get_image_info
from src.transformations import resize_image, crop_image, flip_image, rotate_image, translate_image
from src.color_conversion import (
    convert_to_rgb,
    convert_to_grayscale,
    convert_to_hsv,
    convert_to_lab,
)
from src.annotations import draw_line, draw_rectangle, draw_circle, draw_ellipse, add_text
from src.image_saver import save_image

from src.video_processor import (
    open_video,
    read_frame,
    get_video_info,
    extract_frames,
    save_video_frames,
    process_video_frames,
    process_and_save_video,
)

from src.validation import validate_video_path

from src.image_enhancement import (
    adjust_brightness,
    adjust_contrast,
    apply_gamma_correction,
    apply_negative,
    apply_log_transformation,
    apply_contrast_stretching,
    apply_histogram_equalization,
    apply_clahe,
)

st.set_page_config(page_title="Smart CV Toolkit", page_icon="📷", layout="wide")

st.title("Smart CV Toolkit")

st.write("An interactive toolkit for image and video processing " "using Python and OpenCV.")

st.sidebar.title("Navigation")

page = st.sidebar.selectbox("Choose an operation", ["Home", "Image Processing", "Video Processing"])

if page == "Home":
    st.header("Welcome to Smart CV Toolkit")
    st.write("Upload and process images and videos using OpenCV.")


elif page == "Image Processing":
    st.header("Image Processing")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "bmp", "tiff"])

    if uploaded_file is not None:

        image_bytes = np.frombuffer(uploaded_file.getvalue(), dtype=np.uint8)
        image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

        if image is None:
            st.error("Unable to load the uploaded image.")

        else:
            st.success("Image uploaded successfully!")

            # Save uploaded image temporarily
            temp_path = Path("data/input") / uploaded_file.name
            temp_path.parent.mkdir(parents=True, exist_ok=True)
            temp_path.write_bytes(uploaded_file.getvalue())

            # Image Information
            image_info = get_image_info(image, temp_path)

            st.subheader("Image Information")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Width", image_info["width"])
            col2.metric("Height", image_info["height"])
            col3.metric("Channels", image_info["channels"])
            col4.metric("File Size", f'{image_info["file_size_kb"]} KB')

            with st.expander("More Image Details"):
                st.write("**Shape:**", image_info["shape"])
                st.write("**Data Type:**", image_info["dtype"])

            # Original Image Preview
            st.subheader("Image Preview")

            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            preview_col1, preview_col2 = st.columns(2)

            with preview_col1:
                st.image(image_rgb, caption="Original Image", width=300)

            # Helper: Display, save and download
            def display_result(processed_image, caption, filename="processed_image.png"):
                if processed_image.ndim == 2:
                    display_image = processed_image
                else:
                    display_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)

                with preview_col2:
                    st.image(display_image, caption=caption, width=300)

                st.caption(f"Output shape: {processed_image.shape}")
                st.caption(f"Output data type: {processed_image.dtype}")

                output_path = Path("data/output") / filename

                try:
                    saved_path = save_image(processed_image, output_path)

                    st.success(f"Saved: {saved_path}")

                    extension = saved_path.suffix
                    success, encoded_image = cv2.imencode(extension, processed_image)

                    if success:
                        st.download_button(
                            label="Download Processed Image",
                            data=encoded_image.tobytes(),
                            file_name=saved_path.name,
                            mime=("image/png" if extension == ".png" else "image/jpeg"),
                            key=f"download_{caption}_{filename}",
                        )

                except ValueError as error:
                    st.error(str(error))

            image_height, image_width = image.shape[:2]

            # 1. Geometric Transformations
            with st.expander("1. Geometric Transformations"):

                operation = st.selectbox(
                    "Select operation",
                    ["Resize", "Crop", "Flip", "Rotate", "Translate"],
                    key="geometric_operation",
                )

                if operation == "Resize":
                    resize_width = st.number_input(
                        "Target width", min_value=1, max_value=4000, value=500, key="resize_width"
                    )

                    if st.button("Resize Image"):
                        result = resize_image(image, width=int(resize_width))
                        display_result(result, "Resized Image", "resized_image.png")

                elif operation == "Crop":
                    col1, col2 = st.columns(2)

                    with col1:
                        crop_x = st.number_input(
                            "X coordinate", 0, image_width - 1, 0, key="crop_x"
                        )
                        crop_y = st.number_input(
                            "Y coordinate", 0, image_height - 1, 0, key="crop_y"
                        )

                    with col2:
                        crop_width = st.number_input(
                            "Crop width", 1, image_width, min(400, image_width), key="crop_width"
                        )
                        crop_height = st.number_input(
                            "Crop height",
                            1,
                            image_height,
                            min(400, image_height),
                            key="crop_height",
                        )

                    if st.button("Crop Image"):
                        try:
                            result = crop_image(
                                image, int(crop_x), int(crop_y), int(crop_width), int(crop_height)
                            )
                            display_result(result, "Cropped Image", "cropped_image.png")
                        except ValueError as error:
                            st.error(str(error))

                elif operation == "Flip":
                    direction = st.selectbox(
                        "Flip direction", ["horizontal", "vertical", "both"], key="flip_direction"
                    )

                    if st.button("Flip Image"):
                        result = flip_image(image, direction)
                        display_result(result, "Flipped Image", "flipped_image.png")

                elif operation == "Rotate":
                    angle = st.slider("Rotation angle", -180, 180, 90, key="rotation_angle")

                    if st.button("Rotate Image"):
                        result = rotate_image(image, angle)
                        display_result(result, "Rotated Image", "rotated_image.png")

                elif operation == "Translate":
                    col1, col2 = st.columns(2)

                    with col1:
                        x_shift = st.number_input(
                            "Horizontal shift", -image_width, image_width, 100, key="translate_x"
                        )

                    with col2:
                        y_shift = st.number_input(
                            "Vertical shift", -image_height, image_height, 100, key="translate_y"
                        )

                    if st.button("Translate Image"):
                        result = translate_image(image, int(x_shift), int(y_shift))
                        display_result(result, "Translated Image", "translated_image.png")

            # 2. Color-Space Conversion
            with st.expander("2. Color-Space Conversion"):

                conversion_type = st.selectbox(
                    "Select color space", ["RGB", "Grayscale", "HSV", "Lab"], key="conversion_type"
                )

                if st.button("Convert Color Space"):
                    if conversion_type == "RGB":
                        result = convert_to_rgb(image)
                    elif conversion_type == "Grayscale":
                        result = convert_to_grayscale(image)
                    elif conversion_type == "HSV":
                        result = convert_to_hsv(image)
                    else:
                        result = convert_to_lab(image)

                    display_result(
                        result, f"{conversion_type} Image", f"{conversion_type.lower()}_image.png"
                    )

            # 3. Image Annotation
            with st.expander("3. Image Annotations"):

                annotation_type = st.selectbox(
                    "Select annotation",
                    ["Line", "Rectangle", "Circle", "Ellipse", "Text"],
                    key="annotation_type",
                )

                annotation_color = st.selectbox(
                    "Annotation color",
                    ["Red", "Green", "Blue", "Yellow", "White"],
                    key="annotation_color",
                )

                color_map = {
                    "Red": (0, 0, 255),
                    "Green": (0, 255, 0),
                    "Blue": (255, 0, 0),
                    "Yellow": (0, 255, 255),
                    "White": (255, 255, 255),
                }

                color = color_map[annotation_color]

                thickness = st.slider("Annotation thickness", 1, 20, 3, key="annotation_thickness")

                if annotation_type == "Line":
                    col1, col2 = st.columns(2)

                    with col1:
                        x1 = st.number_input("Start X", 0, image_width - 1, 50, key="line_x1")
                        y1 = st.number_input("Start Y", 0, image_height - 1, 50, key="line_y1")

                    with col2:
                        x2 = st.number_input(
                            "End X", 0, image_width - 1, min(300, image_width - 1), key="line_x2"
                        )
                        y2 = st.number_input(
                            "End Y", 0, image_height - 1, min(300, image_height - 1), key="line_y2"
                        )

                    if st.button("Draw Line"):
                        result = draw_line(
                            image, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness
                        )
                        display_result(result, "Line Annotation", "line_annotation.png")

                elif annotation_type == "Rectangle":
                    col1, col2 = st.columns(2)

                    with col1:
                        x1 = st.number_input("Top-left X", 0, image_width - 1, 50, key="rect_x1")
                        y1 = st.number_input("Top-left Y", 0, image_height - 1, 50, key="rect_y1")

                    with col2:
                        x2 = st.number_input(
                            "Bottom-right X",
                            0,
                            image_width - 1,
                            min(300, image_width - 1),
                            key="rect_x2",
                        )
                        y2 = st.number_input(
                            "Bottom-right Y",
                            0,
                            image_height - 1,
                            min(300, image_height - 1),
                            key="rect_y2",
                        )

                    if st.button("Draw Rectangle"):
                        result = draw_rectangle(
                            image, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness
                        )
                        display_result(result, "Rectangle Annotation", "rectangle_annotation.png")

                elif annotation_type == "Circle":
                    col1, col2 = st.columns(2)

                    with col1:
                        x = st.number_input(
                            "Center X",
                            0,
                            image_width - 1,
                            min(200, image_width - 1),
                            key="circle_x",
                        )
                        y = st.number_input(
                            "Center Y",
                            0,
                            image_height - 1,
                            min(200, image_height - 1),
                            key="circle_y",
                        )

                    with col2:
                        radius = st.number_input(
                            "Radius", 1, max(image_width, image_height), 100, key="circle_radius"
                        )

                    if st.button("Draw Circle"):
                        result = draw_circle(image, (int(x), int(y)), int(radius), color, thickness)
                        display_result(result, "Circle Annotation", "circle_annotation.png")

                elif annotation_type == "Ellipse":
                    col1, col2 = st.columns(2)

                    with col1:
                        x = st.number_input(
                            "Center X",
                            0,
                            image_width - 1,
                            min(200, image_width - 1),
                            key="ellipse_x",
                        )
                        y = st.number_input(
                            "Center Y",
                            0,
                            image_height - 1,
                            min(200, image_height - 1),
                            key="ellipse_y",
                        )

                    with col2:
                        axis_x = st.number_input(
                            "Horizontal axis radius",
                            1,
                            max(image_width, image_height),
                            100,
                            key="ellipse_axis_x",
                        )
                        axis_y = st.number_input(
                            "Vertical axis radius",
                            1,
                            max(image_width, image_height),
                            50,
                            key="ellipse_axis_y",
                        )

                    angle = st.slider("Ellipse angle", 0, 360, 0, key="ellipse_angle")

                    if st.button("Draw Ellipse"):
                        result = draw_ellipse(
                            image,
                            (int(x), int(y)),
                            (int(axis_x), int(axis_y)),
                            angle,
                            color,
                            thickness,
                        )
                        display_result(result, "Ellipse Annotation", "ellipse_annotation.png")

                elif annotation_type == "Text":
                    text = st.text_input("Enter text", "Object", key="annotation_text")

                    col1, col2 = st.columns(2)

                    with col1:
                        x = st.number_input("Text X", 0, image_width - 1, 50, key="text_x")
                        y = st.number_input(
                            "Text Y", 0, image_height - 1, min(100, image_height - 1), key="text_y"
                        )

                    with col2:
                        font_scale = st.slider("Font scale", 0.1, 5.0, 1.0, key="font_scale")

                    if st.button("Add Text"):
                        result = add_text(
                            image, text, (int(x), int(y)), font_scale, color, thickness
                        )
                        display_result(result, "Text Annotation", "text_annotation.png")

            # 4. Image Enhancement
            with st.expander("4. Image Enhancement"):

                enhancement_type = st.selectbox(
                    "Select enhancement technique",
                    [
                        "Brightness Adjustment",
                        "Contrast Adjustment",
                        "Gamma Correction",
                        "Negative Transformation",
                        "Log Transformation",
                        "Contrast Stretching",
                        "Histogram Equalization",
                        "CLAHE",
                    ],
                    key="enhancement_type",
                )

                # Brightness Adjustment
                if enhancement_type == "Brightness Adjustment":

                    beta = st.slider(
                        "Brightness",
                        min_value=-100,
                        max_value=100,
                        value=0,
                        key="enhancement_brightness",
                    )

                    if st.button("Apply Brightness", key="apply_brightness"):
                        result = adjust_brightness(image, beta)

                        display_result(
                            result,
                            "Brightness Adjusted Image",
                            "brightness_image.png",
                        )

                # Contrast Adjustment
                elif enhancement_type == "Contrast Adjustment":

                    alpha = st.slider(
                        "Contrast",
                        min_value=0.1,
                        max_value=3.0,
                        value=1.0,
                        step=0.1,
                        key="enhancement_contrast",
                    )

                    if st.button("Apply Contrast", key="apply_contrast"):
                        result = adjust_contrast(image, alpha)

                        display_result(
                            result,
                            "Contrast Adjusted Image",
                            "contrast_image.png",
                        )

                # Gamma Correction
                elif enhancement_type == "Gamma Correction":

                    gamma = st.slider(
                        "Gamma",
                        min_value=0.1,
                        max_value=3.0,
                        value=1.0,
                        step=0.1,
                        key="enhancement_gamma",
                    )

                    if st.button("Apply Gamma", key="apply_gamma"):
                        result = apply_gamma_correction(image, gamma)

                        display_result(
                            result,
                            "Gamma Corrected Image",
                            "gamma_image.png",
                        )

                # Negative Transformation
                elif enhancement_type == "Negative Transformation":

                    if st.button("Apply Negative", key="apply_negative"):
                        result = apply_negative(image)

                        display_result(
                            result,
                            "Negative Image",
                            "negative_image.png",
                        )

                # Log Transformation
                elif enhancement_type == "Log Transformation":

                    if st.button("Apply Log Transformation", key="apply_log"):
                        result = apply_log_transformation(image)

                        display_result(
                            result,
                            "Log Transformed Image",
                            "log_image.png",
                        )

                # Contrast Stretching
                elif enhancement_type == "Contrast Stretching":

                    if st.button("Apply Contrast Stretching", key="apply_stretch"):
                        result = apply_contrast_stretching(image)

                        display_result(
                            result,
                            "Contrast Stretched Image",
                            "contrast_stretched_image.png",
                        )

                # Histogram Equalization
                elif enhancement_type == "Histogram Equalization":

                    st.info("Histogram Equalization works on grayscale images.")

                    if st.button("Apply Histogram Equalization", key="apply_histogram"):

                        gray_image = convert_to_grayscale(image)

                        result = apply_histogram_equalization(gray_image)

                        display_result(
                            result,
                            "Histogram Equalized Image",
                            "histogram_equalized_image.png",
                        )

                # CLAHE
                elif enhancement_type == "CLAHE":

                    clip_limit = st.slider(
                        "Clip Limit",
                        min_value=1.0,
                        max_value=10.0,
                        value=2.0,
                        step=0.5,
                        key="clahe_clip_limit",
                    )

                    tile_size = st.selectbox(
                        "Tile Grid Size",
                        [(4, 4), (8, 8), (16, 16)],
                        index=1,
                        key="clahe_tile_size",
                    )

                    st.info("CLAHE works on grayscale images.")

                    if st.button("Apply CLAHE", key="apply_clahe"):

                        gray_image = convert_to_grayscale(image)

                        result = apply_clahe(
                            gray_image,
                            clip_limit=clip_limit,
                            tile_grid_size=tile_size,
                        )

                        display_result(
                            result,
                            "CLAHE Enhanced Image",
                            "clahe_image.png",
                        )


elif page == "Video Processing":

    st.header("Video Processing")

    uploaded_video = st.file_uploader("Upload a video", type=["mp4", "avi", "mov", "mkv"])

    if uploaded_video is not None:

        input_video_path = Path("data/input") / uploaded_video.name
        input_video_path.parent.mkdir(parents=True, exist_ok=True)
        input_video_path.write_bytes(uploaded_video.getvalue())

        st.success("Video uploaded successfully!")

        capture = None

        try:
            capture = open_video(input_video_path)

            # Video Information
            video_info = get_video_info(capture)

            st.subheader("Video Information")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Width", video_info["width"])
            col2.metric("Height", video_info["height"])
            col3.metric("FPS", round(video_info["fps"], 2))
            col4.metric("Total Frames", video_info["total_frames"])

            duration = video_info["total_frames"] / video_info["fps"]

            st.caption(
                f'Resolution: {video_info["width"]} x '
                f'{video_info["height"]} | Duration: {duration:.2f} seconds'
            )

            # Original Video Preview
            st.subheader("Video Preview")

            col1, col2, col3 = st.columns([1, 2, 1])

            with col2:
                st.video(uploaded_video.getvalue(), width=400)

            st.divider()

            # 1. Frame Extraction
            with st.expander("1. Frame Extraction"):

                st.write("Extract all frames from the uploaded video.")

                if st.button("Extract All Frames"):

                    capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

                    frames = extract_frames(capture)

                    st.success(f"Extracted {len(frames)} frames successfully!")

                    if frames:
                        display_frame = cv2.cvtColor(frames[0], cv2.COLOR_BGR2RGB)

                        st.image(display_frame, caption="First Extracted Frame", width=300)

            # 2. Save Periodic Frames
            with st.expander("2. Save Frames at Intervals"):

                st.write("Save selected frames at regular intervals.")

                frame_interval = st.number_input(
                    "Frame interval", min_value=1, max_value=1000, value=30, key="frame_interval"
                )

                if st.button("Save Periodic Frames"):

                    capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

                    output_frames_dir = Path("data/output/extracted_frames")

                    saved_frames = save_video_frames(
                        capture, output_frames_dir, interval=int(frame_interval)
                    )

                    st.success(f"Saved {saved_frames} frames to " f"{output_frames_dir}")

            # 3. Process Video Frames
            with st.expander("3. Process Video Frames"):

                st.write("Process every frame in the uploaded video.")

                if st.button("Process Frames"):

                    capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

                    processed_count = process_video_frames(capture)

                    st.success(f"Processed {processed_count} frames successfully!")

            # 4. Grayscale Video Processing
            with st.expander("4. Grayscale Video Processing"):

                st.write(
                    "Convert the uploaded video into grayscale " "and export the processed video."
                )

                if st.button("Process and Save Grayscale Video"):

                    capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

                    output_video_path = Path("data/output/grayscale_video.mp4")

                    processed_count = process_and_save_video(capture, output_video_path)

                    st.success(f"Processed {processed_count} frames successfully!")

                    if output_video_path.exists():

                        st.subheader("Processed Video Preview")

                        col1, col2, col3 = st.columns([1, 2, 1])

                        with col2:
                            st.video(output_video_path.read_bytes(), width=400)

                        st.download_button(
                            label="Download Processed Video",
                            data=output_video_path.read_bytes(),
                            file_name="grayscale_video.mp4",
                            mime="video/mp4",
                        )

        except ValueError as error:
            st.error(str(error))

        finally:
            if capture is not None:
                capture.release()

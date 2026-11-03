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

            # Display original image
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            col1, col2, col3 = st.columns([1, 2, 1])

            with col2:
                st.image(image_rgb, caption="Original Image", width=500)

            # Save uploaded image temporarily
            temp_path = Path("data/input") / uploaded_file.name
            temp_path.parent.mkdir(parents=True, exist_ok=True)
            temp_path.write_bytes(uploaded_file.getvalue())

            # Image Information
            st.subheader("Image Information")

            image_info = get_image_info(image, temp_path)

            col1, col2, col3 = st.columns(3)

            col1.metric("Width", image_info["width"])
            col2.metric("Height", image_info["height"])
            col3.metric("Channels", image_info["channels"])

            st.write("**Shape:**", image_info["shape"])
            st.write("**Data Type:**", image_info["dtype"])
            st.write("**File Size:**", f'{image_info["file_size_kb"]} KB')

            # Helper: Display, save and download
            def display_result(processed_image, caption, filename="processed_image.png"):

                if processed_image.ndim == 2:
                    display_image = processed_image
                else:
                    display_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)

                col1, col2, col3 = st.columns([1, 2, 1])

                with col2:
                    st.image(display_image, caption=caption, width=500)

                st.write("Output shape:", processed_image.shape)
                st.write("Output data type:", processed_image.dtype)

                output_path = Path("data/output") / filename

                try:
                    saved_path = save_image(processed_image, output_path)

                    st.success(f"Image saved to: {saved_path}")

                    extension = saved_path.suffix

                    success, encoded_image = cv2.imencode(extension, processed_image)

                    if success:
                        st.download_button(
                            label="Download Processed Image",
                            data=encoded_image.tobytes(),
                            file_name=saved_path.name,
                            mime="image/png" if extension == ".png" else "image/jpeg",
                            key=f"download_{caption}_{filename}",
                        )

                except ValueError as error:
                    st.error(str(error))

            # 1. Resize
            st.divider()
            st.subheader("1. Resize Image")

            resize_width = st.number_input(
                "Target width", min_value=1, max_value=4000, value=500, key="resize_width"
            )

            if st.button("Resize Image"):
                resized_image = resize_image(image, width=int(resize_width))

                display_result(resized_image, "Resized Image", "resized_image.png")

            # 2. Crop
            st.divider()
            st.subheader("2. Crop Image")

            image_height, image_width = image.shape[:2]

            col1, col2 = st.columns(2)

            with col1:
                crop_x = st.number_input(
                    "X coordinate", min_value=0, max_value=image_width - 1, value=0, key="crop_x"
                )

                crop_y = st.number_input(
                    "Y coordinate", min_value=0, max_value=image_height - 1, value=0, key="crop_y"
                )

            with col2:
                crop_width = st.number_input(
                    "Crop width",
                    min_value=1,
                    max_value=image_width,
                    value=min(400, image_width),
                    key="crop_width",
                )

                crop_height = st.number_input(
                    "Crop height",
                    min_value=1,
                    max_value=image_height,
                    value=min(400, image_height),
                    key="crop_height",
                )

            if st.button("Crop Image"):
                try:
                    cropped_image = crop_image(
                        image, int(crop_x), int(crop_y), int(crop_width), int(crop_height)
                    )

                    display_result(cropped_image, "Cropped Image", "cropped_image.png")

                except ValueError as error:
                    st.error(str(error))

            # 3. Flip
            st.divider()
            st.subheader("3. Flip Image")

            flip_direction = st.selectbox(
                "Select flip direction", ["horizontal", "vertical", "both"]
            )

            if st.button("Flip Image"):
                flipped_image = flip_image(image, flip_direction)

                display_result(flipped_image, "Flipped Image", "flipped_image.png")

            # 4. Rotate
            st.divider()
            st.subheader("4. Rotate Image")

            rotation_angle = st.slider(
                "Select rotation angle", min_value=-180, max_value=180, value=90
            )

            if st.button("Rotate Image"):
                rotated_image = rotate_image(image, rotation_angle)

                display_result(rotated_image, "Rotated Image", "rotated_image.png")

            # 5. Translate
            st.divider()
            st.subheader("5. Translate Image")

            col1, col2 = st.columns(2)

            with col1:
                x_shift = st.number_input(
                    "Horizontal shift (X)",
                    min_value=-image_width,
                    max_value=image_width,
                    value=100,
                    key="translate_x",
                )

            with col2:
                y_shift = st.number_input(
                    "Vertical shift (Y)",
                    min_value=-image_height,
                    max_value=image_height,
                    value=100,
                    key="translate_y",
                )

            if st.button("Translate Image"):
                translated_image = translate_image(image, int(x_shift), int(y_shift))

                display_result(translated_image, "Translated Image", "translated_image.png")

            # 6. Color-Space Conversion
            st.divider()
            st.subheader("6. Color-Space Conversion")

            conversion_type = st.selectbox(
                "Select color space", ["RGB", "Grayscale", "HSV", "Lab"], key="conversion_type"
            )

            if st.button("Convert Color Space"):
                if conversion_type == "RGB":
                    converted_image = convert_to_rgb(image)

                elif conversion_type == "Grayscale":
                    converted_image = convert_to_grayscale(image)

                elif conversion_type == "HSV":
                    converted_image = convert_to_hsv(image)

                else:
                    converted_image = convert_to_lab(image)

                display_result(
                    converted_image,
                    f"{conversion_type} Image",
                    f"{conversion_type.lower()}_image.png",
                )

            # 7. Image Annotation
            st.divider()
            st.subheader("7. Image Annotation")

            annotation_type = st.selectbox(
                "Select annotation",
                ["Line", "Rectangle", "Circle", "Ellipse", "Text"],
                key="annotation_type",
            )

            annotation_color = st.selectbox(
                "Select annotation color", ["Red", "Green", "Blue", "Yellow", "White"]
            )

            color_map = {
                "Red": (0, 0, 255),
                "Green": (0, 255, 0),
                "Blue": (255, 0, 0),
                "Yellow": (0, 255, 255),
                "White": (255, 255, 255),
            }

            color = color_map[annotation_color]

            thickness = st.slider(
                "Annotation thickness",
                min_value=1,
                max_value=20,
                value=3,
                key="annotation_thickness",
            )

            # Line
            if annotation_type == "Line":
                col1, col2 = st.columns(2)

                with col1:
                    x1 = st.number_input("Start X", 0, image_width - 1, 50, key="line_x1")
                    y1 = st.number_input("Start Y", 0, image_height - 1, 50, key="line_y1")

                with col2:
                    x2 = st.number_input("End X", 0, image_width - 1, 300, key="line_x2")
                    y2 = st.number_input("End Y", 0, image_height - 1, 300, key="line_y2")

                if st.button("Draw Line"):
                    result = draw_line(
                        image, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness
                    )

                    display_result(result, "Line Annotation", "line_annotation.png")

            # Rectangle
            elif annotation_type == "Rectangle":
                col1, col2 = st.columns(2)

                with col1:
                    rect_x1 = st.number_input("Top-left X", 0, image_width - 1, 50, key="rect_x1")
                    rect_y1 = st.number_input("Top-left Y", 0, image_height - 1, 50, key="rect_y1")

                with col2:
                    rect_x2 = st.number_input(
                        "Bottom-right X", 0, image_width - 1, 300, key="rect_x2"
                    )
                    rect_y2 = st.number_input(
                        "Bottom-right Y", 0, image_height - 1, 300, key="rect_y2"
                    )

                if st.button("Draw Rectangle"):
                    result = draw_rectangle(
                        image,
                        (int(rect_x1), int(rect_y1)),
                        (int(rect_x2), int(rect_y2)),
                        color,
                        thickness,
                    )

                    display_result(result, "Rectangle Annotation", "rectangle_annotation.png")

            # Circle
            elif annotation_type == "Circle":
                col1, col2 = st.columns(2)

                with col1:
                    circle_x = st.number_input("Center X", 0, image_width - 1, 200, key="circle_x")
                    circle_y = st.number_input("Center Y", 0, image_height - 1, 200, key="circle_y")

                with col2:
                    radius = st.number_input(
                        "Radius",
                        min_value=1,
                        max_value=max(image_width, image_height),
                        value=100,
                        key="circle_radius",
                    )

                if st.button("Draw Circle"):
                    result = draw_circle(
                        image, (int(circle_x), int(circle_y)), int(radius), color, thickness
                    )

                    display_result(result, "Circle Annotation", "circle_annotation.png")

            # Ellipse
            elif annotation_type == "Ellipse":
                col1, col2 = st.columns(2)

                with col1:
                    ellipse_x = st.number_input(
                        "Center X", 0, image_width - 1, 200, key="ellipse_x"
                    )
                    ellipse_y = st.number_input(
                        "Center Y", 0, image_height - 1, 200, key="ellipse_y"
                    )

                with col2:
                    axis_x = st.number_input(
                        "Horizontal axis radius", min_value=1, value=100, key="ellipse_axis_x"
                    )
                    axis_y = st.number_input(
                        "Vertical axis radius", min_value=1, value=50, key="ellipse_axis_y"
                    )

                ellipse_angle = st.slider(
                    "Ellipse angle",
                    min_value=0,
                    max_value=360,
                )

                if st.button("Draw Ellipse"):
                    result = draw_ellipse(
                        image,
                        (int(ellipse_x), int(ellipse_y)),
                        (int(axis_x), int(axis_y)),
                        ellipse_angle,
                        color,
                        thickness,
                    )

                    display_result(result, "Ellipse Annotation", "ellipse_annotation.png")

            # Text
            elif annotation_type == "Text":
                annotation_text = st.text_input("Enter text", value="Object", key="annotation_text")

                col1, col2 = st.columns(2)

                with col1:
                    text_x = st.number_input("Text X", 0, image_width - 1, 50, key="text_x")
                    text_y = st.number_input("Text Y", 0, image_height - 1, 100, key="text_y")

                with col2:
                    font_scale = st.slider(
                        "Font scale", min_value=0.1, max_value=5.0, value=1.0, key="font_scale"
                    )

                if st.button("Add Text"):
                    result = add_text(
                        image,
                        annotation_text,
                        (int(text_x), int(text_y)),
                        font_scale,
                        color,
                        thickness,
                    )

                    display_result(result, "Text Annotation", "text_annotation.png")


elif page == "Video Processing":

    st.header("Video Processing")

    uploaded_video = st.file_uploader("Upload a video", type=["mp4", "avi", "mov", "mkv"])

    if uploaded_video is not None:

        # Save uploaded video
        input_video_path = Path("data/input") / uploaded_video.name

        input_video_path.parent.mkdir(parents=True, exist_ok=True)

        input_video_path.write_bytes(uploaded_video.getvalue())

        st.success("Video uploaded successfully!")

        try:
            capture = open_video(input_video_path)

            # Video Information
            st.subheader("Video Information")

            video_info = get_video_info(capture)

            col1, col2, col3 = st.columns(3)

            col1.metric("Width", video_info["width"])
            col2.metric("Height", video_info["height"])
            col3.metric("FPS", round(video_info["fps"], 2))

            st.metric("Total Frames", video_info["total_frames"])

            st.write("**Resolution:**", f'{video_info["width"]} x {video_info["height"]}')

            st.write(
                "**Duration:**", f'{video_info["total_frames"] / video_info["fps"]:.2f} seconds'
            )

            # Original Video Preview
            st.subheader("Video Preview")

            col1, col2, col3 = st.columns([1, 2, 1])

            with col2:
                st.video(uploaded_video.getvalue(), width=500)

            st.divider()

            # 1. Frame Extraction
            st.subheader("1. Frame Extraction")

            if st.button("Extract All Frames"):

                capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

                frames = extract_frames(capture)

                st.success(f"Extracted {len(frames)} frames successfully!")

                if frames:

                    display_frame = cv2.cvtColor(frames[0], cv2.COLOR_BGR2RGB)

                    col1, col2, col3 = st.columns([1, 2, 1])

                    with col2:
                        st.image(display_frame, caption="First Extracted Frame", width=500)

            # 2. Save Periodic Frames
            st.divider()
            st.subheader("2. Save Frames at Intervals")

            frame_interval = st.number_input(
                "Frame interval", min_value=1, max_value=1000, value=30, key="frame_interval"
            )

            if st.button("Save Periodic Frames"):

                capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

                output_frames_dir = Path("data/output/extracted_frames")

                saved_frames = save_video_frames(
                    capture, output_frames_dir, interval=int(frame_interval)
                )

                st.success(f"Periodic frames saved to {output_frames_dir}")

            # 3. Process Video Frames
            st.divider()
            st.subheader("3. Process Video Frames")

            if st.button("Process Frames"):

                capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

                processed_count = process_video_frames(capture)

                st.success(f"Processed {processed_count} frames successfully!")

            # 4. Grayscale Video Processing
            st.divider()
            st.subheader("4. Grayscale Video Processing")

            if st.button("Process and Save Grayscale Video"):

                capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

                output_video_path = Path("data/output/grayscale_video.mp4")

                processed_count = process_and_save_video(capture, output_video_path)

                st.success(f"Processed {processed_count} frames successfully!")

                if output_video_path.exists():

                    st.subheader("Processed Video Preview")

                    col1, col2, col3 = st.columns([1, 2, 1])

                    with col2:
                        st.video(output_video_path.read_bytes(), width=500)

                    st.download_button(
                        label="Download Processed Video",
                        data=output_video_path.read_bytes(),
                        file_name="grayscale_video.mp4",
                        mime="video/mp4",
                    )

            capture.release()

        except ValueError as error:
            st.error(str(error))

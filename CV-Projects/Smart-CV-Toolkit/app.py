import cv2
import numpy as np
import streamlit as st
from pathlib import Path
from src.image_info import get_image_info
from src.transformations import resize_image, crop_image, flip_image, rotate_image, translate_image

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

            # Display original image at a fixed width
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            col1, col2, col3 = st.columns([1, 2, 1])

            with col2:
                st.image(image_rgb, caption="Original Image", width=500)

            # Save uploaded image temporarily
            temp_path = Path("data/input") / uploaded_file.name

            temp_path.parent.mkdir(parents=True, exist_ok=True)

            temp_path.write_bytes(uploaded_file.getvalue())

            # Image information
            st.subheader("Image Information")

            image_info = get_image_info(image, temp_path)

            col1, col2, col3 = st.columns(3)

            col1.metric("Width", image_info["width"])
            col2.metric("Height", image_info["height"])
            col3.metric("Channels", image_info["channels"])

            st.write("**Shape:**", image_info["shape"])
            st.write("**Data Type:**", image_info["dtype"])
            st.write("**File Size:**", f'{image_info["file_size_kb"]} KB')

            st.divider()
            st.subheader("Image Transformations")

            # Display processed images at a fixed width
            def display_result(processed_image, caption):
                processed_rgb = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)

                col1, col2, col3 = st.columns([1, 2, 1])

                with col2:
                    st.image(processed_rgb, caption=caption, width=500)

                st.write("Output shape:", processed_image.shape)

            # 1. Resize
            st.markdown("### 1. Resize Image")

            resize_width = st.number_input(
                "Target width", min_value=1, max_value=4000, value=500, key="resize_width"
            )

            if st.button("Resize Image"):
                resized_image = resize_image(image, width=int(resize_width))

                display_result(resized_image, "Resized Image")

            # 2. Crop
            st.markdown("### 2. Crop Image")

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

                    display_result(cropped_image, "Cropped Image")

                except ValueError as error:
                    st.error(str(error))

            # 3. Flip
            st.markdown("### 3. Flip Image")

            flip_direction = st.selectbox(
                "Select flip direction", ["horizontal", "vertical", "both"]
            )

            if st.button("Flip Image"):
                flipped_image = flip_image(image, flip_direction)

                display_result(flipped_image, "Flipped Image")

            # 4. Rotate
            st.markdown("### 4. Rotate Image")

            rotation_angle = st.slider(
                "Select rotation angle", min_value=-180, max_value=180, value=90
            )

            if st.button("Rotate Image"):
                rotated_image = rotate_image(image, rotation_angle)

                display_result(rotated_image, "Rotated Image")

            # 5. Translate
            st.markdown("### 5. Translate Image")

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

                display_result(translated_image, "Translated Image")

# elif page == "Image Processing":
#     st.header("Image Processing")

#     uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "bmp", "tiff"])

#     if uploaded_file is not None:

#         # Decode uploaded image
#         image_bytes = np.frombuffer(uploaded_file.getvalue(), dtype=np.uint8)

#         image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

#         if image is None:
#             st.error("Unable to load the uploaded image.")

#         else:
#             st.success("Image uploaded successfully!")

#             # Display original image
#             image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#             st.image(image_rgb, caption="Original Image", use_container_width=True)

#             # Save uploaded image temporarily
#             temp_path = Path("data/input") / uploaded_file.name

#             temp_path.parent.mkdir(parents=True, exist_ok=True)

#             temp_path.write_bytes(uploaded_file.getvalue())

#             # Image information
#             st.subheader("Image Information")

#             image_info = get_image_info(image, temp_path)

#             col1, col2, col3 = st.columns(3)

#             col1.metric("Width", image_info["width"])
#             col2.metric("Height", image_info["height"])
#             col3.metric("Channels", image_info["channels"])

#             st.write("**Shape:**", image_info["shape"])
#             st.write("**Data Type:**", image_info["dtype"])
#             st.write("**File Size:**", f'{image_info["file_size_kb"]} KB')

#             # Image transformations
#             st.divider()
#             st.subheader("Image Transformations")

#             # Helper function to display processed images
#             def display_result(processed_image, caption):
#                 processed_rgb = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)

#                 st.image(processed_rgb, caption=caption, use_container_width=True)

#                 st.write("Output shape:", processed_image.shape)

#             # 1. Resize
#             st.markdown("### 1. Resize Image")

#             resize_width = st.number_input(
#                 "Target width", min_value=1, max_value=4000, value=500, key="resize_width"
#             )

#             if st.button("Resize Image"):
#                 resized_image = resize_image(image, width=int(resize_width))

#                 display_result(resized_image, "Resized Image")

#             # 2. Crop
#             st.markdown("### 2. Crop Image")

#             image_height, image_width = image.shape[:2]

#             col1, col2 = st.columns(2)

#             with col1:
#                 crop_x = st.number_input(
#                     "X coordinate", min_value=0, max_value=image_width - 1, value=0, key="crop_x"
#                 )

#                 crop_y = st.number_input(
#                     "Y coordinate", min_value=0, max_value=image_height - 1, value=0, key="crop_y"
#                 )

#             with col2:
#                 crop_width = st.number_input(
#                     "Crop width",
#                     min_value=1,
#                     max_value=image_width,
#                     value=min(400, image_width),
#                     key="crop_width",
#                 )

#                 crop_height = st.number_input(
#                     "Crop height",
#                     min_value=1,
#                     max_value=image_height,
#                     value=min(400, image_height),
#                     key="crop_height",
#                 )

#             if st.button("Crop Image"):
#                 try:
#                     cropped_image = crop_image(
#                         image, int(crop_x), int(crop_y), int(crop_width), int(crop_height)
#                     )

#                     display_result(cropped_image, "Cropped Image")

#                 except ValueError as error:
#                     st.error(str(error))

#             # 3. Flip
#             st.markdown("### 3. Flip Image")

#             flip_direction = st.selectbox(
#                 "Select flip direction", ["horizontal", "vertical", "both"]
#             )

#             if st.button("Flip Image"):
#                 flipped_image = flip_image(image, flip_direction)

#                 display_result(flipped_image, "Flipped Image")

#             # 4. Rotate
#             st.markdown("### 4. Rotate Image")

#             rotation_angle = st.slider(
#                 "Select rotation angle", min_value=-180, max_value=180, value=90
#             )

#             if st.button("Rotate Image"):
#                 rotated_image = rotate_image(image, rotation_angle)

#                 display_result(rotated_image, "Rotated Image")

#             # 5. Translate
#             st.markdown("### 5. Translate Image")

#             col1, col2 = st.columns(2)

#             with col1:
#                 x_shift = st.number_input(
#                     "Horizontal shift (X)",
#                     min_value=-image_width,
#                     max_value=image_width,
#                     value=100,
#                     key="translate_x",
#                 )

#             with col2:
#                 y_shift = st.number_input(
#                     "Vertical shift (Y)",
#                     min_value=-image_height,
#                     max_value=image_height,
#                     value=100,
#                     key="translate_y",
#                 )

#             if st.button("Translate Image"):
#                 translated_image = translate_image(image, int(x_shift), int(y_shift))

#                 display_result(translated_image, "Translated Image")

elif page == "Video Processing":
    st.header("Video Processing")
    st.info("Video processing features will be added here.")

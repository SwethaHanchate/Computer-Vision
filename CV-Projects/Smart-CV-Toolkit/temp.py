# from src.image_loader import load_image
# from src.transformations import resize_image, crop_image, flip_image, rotate_image, translate_image
# import cv2

# image = load_image("data/input/sample.jpeg")

# resized = resize_image(image, width=500)
# cropped = crop_image(image, 100, 100, 400, 500)
# flipped = flip_image(image, "horizontal")
# rotated = rotate_image(image, 45)
# translated = translate_image(image, 100, 50)

# # print("Original:", image.shape)
# # print("Resized:", resized.shape)
# # print("Cropped:", cropped.shape)
# # print("Flipped:", flipped.shape)
# # print("Rotated:", rotated.shape)
# # print("Translated:", translated.shape)

# from src.color_conversion import (
#     convert_to_rgb,
#     convert_to_grayscale,
#     convert_to_hsv,
#     convert_to_lab,
# )

# rgb = convert_to_rgb(image)
# gray = convert_to_grayscale(image)
# hsv = convert_to_hsv(image)
# lab = convert_to_lab(image)

# # print("Original:", image.shape)
# # print("RGB:", rgb.shape)
# # print("Grayscale:", gray.shape)
# # print("HSV:", hsv.shape)
# # print("Lab:", lab.shape)


# from src.annotations import draw_line, draw_rectangle, draw_circle, draw_ellipse, add_text

# annotated = draw_line(image, (50, 50), (600, 300))

# annotated = draw_rectangle(annotated, (100, 350), (500, 900))

# annotated = draw_circle(annotated, (550, 600), 80)

# annotated = draw_ellipse(annotated, (350, 1100), (150, 70), angle=30)

# annotated = add_text(annotated, "Computer Vision", (100, 1200), font_scale=1.5)

# from src.image_saver import save_image

# saved_path = save_image(annotated, "data/output/annotated_image.jpg")

# # print("Original:", image.shape)
# # print("Final annotated:", annotated.shape)
# # print("All annotations completed!")

# # print("Saved at:", saved_path)
# # print("File exists:", saved_path.exists())


# # cv2.imshow("Annotated", text)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()


from pathlib import Path

print("Current directory:", Path.cwd())
print("Input folder exists:", Path("data/input").exists())
print("Files:", list(Path("data/input").glob("*")))

from src.video_processor import (
    open_video,
    read_frame,
    get_video_info,
    extract_frames,
    save_video_frames,
    process_video_frames,
    process_and_save_video,
)

video = open_video("data/input/sample.mp4")

# frame = read_frame(video)

# if frame is not None:
#     print("Frame extracted:", frame.shape)
# else:
#     print("No frame available")

# info = get_video_info(video)
# # for key, value in info.items():
# #     print(f"{key}: {value}")

# frames = extract_frames(video)
# # print("Total extracted frames:", len(frames))
# # print("First frame shape:", frames[0].shape)

# saved_count = save_video_frames(video, "data/output/frames", interval=30)
# print("Frames saved:", saved_count)

# processed_count = process_video_frames(video)
# print("Total processed frames:", processed_count)


processed_count = process_and_save_video(video, "data/output/grayscale_video.mp4")


video.release()
print("Processed frames:", processed_count)
print("Output video saved successfully!")

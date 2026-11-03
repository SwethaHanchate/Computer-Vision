# Smart CV Toolkit

An interactive Computer Vision toolkit built using Python, OpenCV, NumPy, and Streamlit. This application provides a user-friendly interface for exploring image and video processing operations.

## Application Screenshots

### Home
![Home](screenshots/home.png)

### Image Processing
![Image Processing](screenshots/image_processing/image_processing.png)

#### Geometric Transformations
| Resize | Crop |
|---|---|
| ![Resize](screenshots/image_processing/transformations/resized.png) | ![Crop](screenshots/image_processing/transformations/cropped.png) |

| Flip | Rotate | Translate |
|---|---|---|
| ![Flip](screenshots/image_processing/transformations/flipped.png) | ![Rotate](screenshots/image_processing/transformations/rotated.png) | ![Translate](screenshots/image_processing/transformations/translated.png) |

#### Color-Space Conversion
| RGB | Grayscale |
|---|---|
| ![RGB](screenshots/image_processing/color_conversions/rgb.png) | ![Grayscale](screenshots/image_processing/color_conversions/grayscale.png) |

| HSV | Lab |
|---|---|
| ![HSV](screenshots/image_processing/color_conversions/hsv.png) | ![Lab](screenshots/image_processing/color_conversions/lab.png) |

#### Image Annotations
| Line | Rectangle |
|---|---|
| ![Line](screenshots/image_processing/annotations/line.png) | ![Rectangle](screenshots/image_processing/annotations/rectangle.png) |

| Circle | Ellipse | Text |
|---|---|---|
| ![Circle](screenshots/image_processing/annotations/circle.png) | ![Ellipse](screenshots/image_processing/annotations/ellipse.png) | ![Text](screenshots/image_processing/annotations/text.png) |

### Video Processing
![Video Processing](screenshots/video_processing/video_processing.png)

#### Video Features
![Video Features](screenshots/video_processing/video_features.png)

#### Grayscale Video Processing
![Processed Video](screenshots/video_processing/processed_video.png)

## Features

### Image Processing
- Image upload and metadata extraction
- Image resizing and cropping
- Horizontal, vertical, and combined flipping
- Image rotation and translation
- RGB, Grayscale, HSV, and Lab conversion
- Image annotations: lines, rectangles, circles, ellipses, and text
- Save and download processed images

### Video Processing
- Video upload and preview
- Video metadata extraction
- Frame extraction
- Periodic frame saving
- Video frame processing
- Grayscale video conversion
- Save and download processed videos

## Tech Stack

- Python
- OpenCV
- NumPy
- Streamlit

## Project Structure

```text
Smart-CV-Toolkit/
├── app.py
├── src/
├── data/
├── screenshots/
│   ├── home.png
│   ├── image_processing/
│   │   ├── annotations/
│   │   ├── color_conversions/
│   │   └── transformations/
│   └── video_processing/
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Smart-CV-Toolkit
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

macOS / Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
streamlit run app.py
```

## Future Enhancements

- Image filtering and enhancement
- Edge detection and thresholding
- Morphological operations
- Image segmentation
- Object detection integration
- Real-time webcam processing

## Author

Swetha Hanchate
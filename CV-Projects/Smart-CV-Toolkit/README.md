
# Smart CV Toolkit

An interactive Computer Vision toolkit built using Python, OpenCV, NumPy, and Streamlit. It provides a simple interface for image and video processing operations.

## Features

### Image Processing
- Image upload and metadata extraction
- Image resizing and cropping
- Horizontal and vertical flipping
- Image rotation and translation
- Color-space conversion:
  - RGB
  - Grayscale
  - HSV
  - Lab
- Image annotations:
  - Lines
  - Rectangles
  - Circles
  - Ellipses
  - Text labels
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
│   ├── __init__.py
│   ├── image_loader.py
│   ├── image_info.py
│   ├── transformations.py
│   ├── color_conversion.py
│   ├── annotations.py
│   ├── video_processor.py
│   ├── validation.py
│   └── image_saver.py
├── data/
│   ├── input/
│   └── output/
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

The application will open in your browser.

## Usage

1. Select Image Processing or Video Processing from the sidebar.
2. Upload an image or video.
3. Select the operation you want to perform.
4. View the processed result.
5. Save or download the output.

## Learning Outcomes

This project demonstrates practical implementation of:

- Image representation and processing using NumPy and OpenCV
- Geometric image transformations
- Color-space conversions
- Image annotation techniques
- Video capture and frame extraction
- Video processing and encoding
- Input validation and error handling
- Building interactive Computer Vision applications

## Future Enhancements

- Image filtering and enhancement
- Edge detection and thresholding
- Image segmentation
- Object detection integration
- Real-time webcam processing

## Author

Swetha Hanchate

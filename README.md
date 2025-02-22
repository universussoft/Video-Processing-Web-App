# Video Processing Web App

This is a Flask-based web application for processing videos. It allows users to:
- Upload a video
- Crop the video
- Reverse the video
- Resize the video duration
- Merge multiple videos
- Extract frames from a video

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Setting Up FFmpeg](#setting-up-ffmpeg)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Requirements
- Python 3.8 or higher
- FFmpeg (installed locally or downloaded via the provided script)
- Flask
- OpenCV (opencv-python)
- NumPy

## Installation

### Clone the Repository:
```bash
git clone https://github.com/universussoft/Video-Processing-Web-App.git
cd Video-Processing-Web-App
```

### Install Python Dependencies:
Install the required Python packages using pip:
```bash
pip install -r requirements.txt
```
The `requirements.txt` file should contain:
```
Flask==2.3.2
opencv-python==4.8.1.78
numpy==1.26.0
```

### Set Up the Environment:
Create the necessary folders:
```bash
mkdir uploads processed bin
```

## Setting Up FFmpeg
FFmpeg is required for video processing. You can either install it globally or download it into the `bin` folder using the provided script.

### Option 1: Download FFmpeg Using the Script
Run the `download_ffmpeg.py` script to download FFmpeg for your operating system:
```bash
python download_ffmpeg.py
```

#### Extract the Files:
- **Windows:** Extract `ffmpeg-release-essentials.zip` and copy `ffmpeg.exe` and `ffprobe.exe` from the `bin` folder inside the archive to your project’s `bin` folder.
- **Linux:** Extract `ffmpeg-release-i686-static.tar.xz` and copy `ffmpeg` and `ffprobe` to the `bin` folder.
- **macOS:** Extract `ffmpeg.zip` and copy `ffmpeg` and `ffprobe` to the `bin` folder.

Verify FFmpeg is in the `bin` folder:
```
bin/
├── ffmpeg
├── ffprobe
```

### Option 2: Install FFmpeg Globally
If you prefer to install FFmpeg globally, follow these steps:
- **Windows:** Download FFmpeg from [FFmpeg Official Site](https://ffmpeg.org/download.html), extract the files, and add the `bin` folder to your system's PATH.
- **Linux:**
  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```
- **macOS:**
  ```bash
  brew install ffmpeg
  ```

## Running the Application
Start the Flask application:
```bash
python app.py
```

Access the web app in your browser:
```
http://127.0.0.1:5000
```

### Upload a Video
Use the web interface to upload a video file. The app will process the video and display the results.

## Project Structure
```
Video-Processing-Web-App/
│
├── app.py                  # Main Flask application
├── download_ffmpeg.py      # Script to download FFmpeg
├── requirements.txt        # Python dependencies
├── bin/                    # Folder for FFmpeg executables
├── uploads/                # Folder for uploaded videos
├── processed/              # Folder for processed videos
├── templates/              # HTML templates
│   ├── index.html          # Home page
│   └── results.html        # Results page
└── README.md               # This file
```

## Troubleshooting

### 1. FFmpeg Not Found
- Ensure the `bin` folder contains `ffmpeg` and `ffprobe`.
- Verify that the `bin` folder is added to the system's PATH or that the `download_ffmpeg.py` script has been used correctly.

### 2. Dependency Errors
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### 3. Video Processing Errors
- Ensure the uploaded video file is valid and supported by FFmpeg.
- Check the logs for detailed error messages.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

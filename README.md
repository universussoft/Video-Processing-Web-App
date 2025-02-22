Video Processing Web App
This is a Flask-based web application for processing videos. It allows users to upload a video, crop it, reverse it, resize its duration, merge videos, and extract frames.

Table of Contents
Requirements

Installation

Setting Up FFmpeg

Running the Application

Project Structure

Troubleshooting

Requirements
Python 3.8 or higher

FFmpeg (installed locally or downloaded via the provided script)

Flask

OpenCV (opencv-python)

NumPy

Installation
Clone the Repository:

bash
Copy
git clone https://github.com/universussoft/Video-Processing-Web-App.git
cd Video-Processing-Web-App
Install Python Dependencies:
Install the required Python packages using pip:

bash
Copy
pip install -r requirements.txt
The requirements.txt file should contain:

Copy
Flask==2.3.2
opencv-python==4.8.1.78
numpy==1.26.0
Set Up the Environment:

Create the necessary folders:

bash
Copy
mkdir uploads processed bin
Setting Up FFmpeg
FFmpeg is required for video processing. You can either install it globally or download it into the bin folder using the provided script.

Option 1: Download FFmpeg Using the Script
Run the download_ffmpeg.py script to download FFmpeg for your operating system:

bash
Copy
python download_ffmpeg.py
Extract the Files:

Windows:

Extract the downloaded ffmpeg-release-essentials.zip file.

Copy ffmpeg.exe and ffprobe.exe from the bin folder inside the extracted archive to the bin folder in your project.

Linux:

Extract the downloaded ffmpeg-release-i686-static.tar.xz file.

Copy ffmpeg and ffprobe from the extracted folder to the bin folder in your project.

macOS:

Extract the downloaded ffmpeg.zip file.

Copy ffmpeg and ffprobe from the extracted folder to the bin folder in your project.

Verify FFmpeg:
Ensure the bin folder contains the FFmpeg executables:

Copy
bin/
├── ffmpeg
├── ffprobe
Option 2: Install FFmpeg Globally
If you prefer to install FFmpeg globally, follow these steps:

Windows:

Download FFmpeg from https://ffmpeg.org/download.html.

Extract the files and add the bin folder to your system's PATH.

Linux:

bash
Copy
sudo apt update
sudo apt install ffmpeg
macOS:

bash
Copy
brew install ffmpeg
Running the Application
Start the Flask Application:

bash
Copy
python app.py
Access the Web App:
Open your browser and navigate to:

Copy
http://127.0.0.1:5000
Upload a Video:

Use the web interface to upload a video file.

The app will process the video and display the results.

Project Structure
Copy
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
Troubleshooting
1. FFmpeg Not Found
Ensure the bin folder contains ffmpeg and ffprobe.

Verify that the bin folder is added to the system's PATH or that the download_ffmpeg.py script is used correctly.

2. Dependency Errors
Make sure all dependencies are installed:

bash
Copy
pip install -r requirements.txt
3. Video Processing Errors
Ensure the uploaded video file is valid and supported by FFmpeg.

Check the logs for detailed error messages.

License
This project is licensed under the MIT License. See the LICENSE file for details.

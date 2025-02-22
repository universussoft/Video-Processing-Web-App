import os
import sys
import shutil
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import cv2
import subprocess

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'

# Add the bin folder to the system PATH
bin_path = os.path.join(os.path.dirname(__file__), 'bin')
os.environ['PATH'] += os.pathsep + bin_path

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

def check_ffmpeg_installed():
    """Check if ffmpeg and ffprobe are installed and accessible."""
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        return False
    return True

def crop_video(input_path, output_path):
    try:
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            return "Error: Cannot open video file"

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        new_width = int(height * (9 / 16))
        start_x = (width - new_width) // 2

        ffmpeg_command = [
            "ffmpeg", "-i", input_path, "-vf",
            f"crop={new_width}:{height}:{start_x}:0",
            "-c:v", "libx264", "-crf", "23", "-preset", "fast",
            "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
            output_path
        ]

        subprocess.run(ffmpeg_command, check=True)
        return f"✅ Video saved: {output_path}"
    except subprocess.CalledProcessError as e:
        return f"Error cropping video: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

def reverse_video(input_path, output_path):
    try:
        ffmpeg_command = [
            "ffmpeg", "-i", input_path, "-vf", "reverse", "-af", "areverse",
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            "-movflags", "+faststart", output_path
        ]

        subprocess.run(ffmpeg_command, check=True)
        return f"✅ Reversed video saved: {output_path}"
    except subprocess.CalledProcessError as e:
        return f"Error reversing video: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

def get_video_duration(video_path):
    try:
        command = f"ffprobe -i \"{video_path}\" -show_entries format=duration -v quiet -of csv=\"p=0\""
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return float(result.stdout.strip())
    except ValueError:
        return None
    except Exception as e:
        print(f"Error getting video duration: {e}")
        return None

def has_audio_stream(video_path):
    try:
        command = f"ffprobe -i \"{video_path}\" -show_streams -select_streams a -loglevel error"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return bool(result.stdout.strip())
    except Exception as e:
        print(f"Error checking audio stream: {e}")
        return False

def resize_video_duration(input_video, output_video, target_duration=8):
    try:
        original_duration = get_video_duration(input_video)
        if original_duration is None:
            return "Error: Could not retrieve video duration."

        speed_factor = original_duration / target_duration
        has_audio = has_audio_stream(input_video)

        if has_audio:
            ffmpeg_command = (
                f"ffmpeg -i \"{input_video}\" -filter_complex "
                f"\"[0:v]setpts={1/speed_factor}*PTS[v];[0:a]atempo={speed_factor}[a]\" "
                f"-map \"[v]\" -map \"[a]\" -c:v libx264 -preset fast -c:a aac -b:a 128k \"{output_video}\""
            )
        else:
            ffmpeg_command = (
                f"ffmpeg -i \"{input_video}\" -filter_complex "
                f"\"[0:v]setpts={1/speed_factor}*PTS\" "
                f"-an -c:v libx264 -preset fast \"{output_video}\""
            )

        os.system(ffmpeg_command)
        return f"Resized video saved to {output_video}"
    except Exception as e:
        return f"Error resizing video: {e}"

def merge_videos_ffmpeg(video1_path, video2_path, output_path):
    try:
        list_file = "video_list.txt"
        with open(list_file, "w") as f:
            f.write(f"file '{video1_path}'\n")
            f.write(f"file '{video2_path}'\n")
        
        command = f"ffmpeg -f concat -safe 0 -i {list_file} -c copy {output_path}"
        os.system(command)

        os.remove(list_file)
        return f"Videos merged successfully with audio: {output_path}"
    except Exception as e:
        return f"Error merging videos: {e}"

def extract_frames(video_path, output_folder, frame_interval=1):
    try:
        os.makedirs(output_folder, exist_ok=True)
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return "Error: Could not open video."

        frame_count = 0
        saved_count = 0
        
        while True:
            success, frame = cap.read()
            if not success:
                break
            
            if frame_count % frame_interval == 0:
                frame_filename = os.path.join(output_folder, f"frame_{saved_count:06d}.jpg")
                cv2.imwrite(frame_filename, frame)
                saved_count += 1
            
            frame_count += 1
        
        cap.release()
        return f"Extracted {saved_count} frames to '{output_folder}'"
    except Exception as e:
        return f"Error extracting frames: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect(url_for('process_video', filename=file.filename))

@app.route('/process/<filename>')
def process_video(filename):
    if not check_ffmpeg_installed():
        return "Error: FFmpeg or FFprobe is not installed. Please ensure the bin folder is correctly set up."

    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    cropped_path = os.path.join(app.config['PROCESSED_FOLDER'], 'cropped_' + filename)
    reversed_path = os.path.join(app.config['PROCESSED_FOLDER'], 'reversed_' + filename)
    resized_path = os.path.join(app.config['PROCESSED_FOLDER'], 'resized_' + filename)
    merged_path = os.path.join(app.config['PROCESSED_FOLDER'], 'merged_' + filename)
    frames_folder = os.path.join(app.config['PROCESSED_FOLDER'], 'frames_' + filename)

    crop_result = crop_video(input_path, cropped_path)
    reverse_result = reverse_video(cropped_path, reversed_path)
    resize_result = resize_video_duration(reversed_path, resized_path)
    merge_result = merge_videos_ffmpeg(cropped_path, reversed_path, merged_path)
    extract_result = extract_frames(resized_path, frames_folder)

    return render_template('results.html', crop_result=crop_result, reverse_result=reverse_result, resize_result=resize_result, merge_result=merge_result, extract_result=extract_result)

@app.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
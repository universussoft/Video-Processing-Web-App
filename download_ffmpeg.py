import os
import platform
import urllib.request

def download_ffmpeg():
    system = platform.system()
    if system == "Windows":
        url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    elif system == "Linux":
        url = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-i686-static.tar.xz"
    elif system == "Darwin":
        url = "https://evermeet.cx/ffmpeg/ffmpeg.zip"
    else:
        raise Exception("Unsupported OS")

    filename = url.split("/")[-1]
    print(f"Downloading FFmpeg from {url}...")
    urllib.request.urlretrieve(url, filename)
    print("Download complete.")

if __name__ == "__main__":
    download_ffmpeg()
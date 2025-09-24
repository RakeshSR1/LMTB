import os
import subprocess
import platform

# Check OS
yt_dlp_bin = "yt-dlp.exe" if platform.system() == "Windows" else "yt-dlp"

# Full path to yt-dlp in the same folder as this script
YT_DLP_PATH = os.path.join(os.path.dirname(__file__), yt_dlp_bin)

# Example: list formats of a video
url = "https://youtube.com/watch?v=example"
subprocess.run([YT_DLP_PATH, "-F", url])

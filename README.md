# Youtube Album Downloader
This script downloads entire YouTube Music albums by prodividing a link and tags and files them using YouTube Music API. By default, it will download tracks at AAC 128k, but it can also do AAC 256k if a YouTube Music Premium cookies.txt is placed at the same directory as this script.

### Requirements
    pip install yt_dlp mutagen ytmusicapi
You will also need ffmpeg installed in your system.

### Know issues
* It can't download tracks that exceeds the Windows file length limit. The current workaround is to run the script on WSL.
    
Special thanks to Patrick Timm for helping me out in this project.

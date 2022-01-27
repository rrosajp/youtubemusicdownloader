# YouTube Musi Downloader
This script downloads entire YouTube Music albums, playlists or tracks by prodividing a link. It tags and names them using YouTube Music API. By default, tracks will be downloaded at AAC 128k, but it can also do AAC 256k if a YouTube Music Premium cookies.txt is placed at the same directory as this script.

### Requirements
    pip install yt_dlp mutagen ytmusicapi
You will also need ffmpeg installed in your system.

### Know issues
* It can't download tracks that exceeds the Windows file length limit. The current workaround is to run the script on WSL.
    
Special thanks to Patrick Timm for helping me out in this project.

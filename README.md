# YouTube Music Downloader
A simple Python script to download YouTube Music playlists, albums or tracks by providing a link. By default, tracks are downloaded at AAC 128k, but you can also get AAC 256k if a YouTube Music Premium cookies.txt is placed at the same directory as this script. Tags (album artist, album cover, album name, album track count, album year, track artist, track lyrics, track name, track number, track rating) are fetched from YouTube Music itself.

### Requirements
    pip install yt_dlp mutagen ytmusicapi
You will also need ffmpeg installed in your system.

### Usage
    python youtubemusicdownload "(link)"    (Support multiple link inputs)

Special thanks to Patrick Timm for helping me out in this project.

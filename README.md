# YouTube Music Downloader
A simple Python script to download YouTube Music playlists, albums or tracks by providing a link.
By default, tracks are downloaded in AAC 128k codec, but you can get AAC 256k if you place a YouTube Music Premium cookies.txt at the same directory as this script.
You can also download tracks in Opus codec by typing "opus" on the last argument.
Tags (album artist, album cover, album name, album track count, album year, track artist, track lyrics, track name, track number, track rating) are fetched from YouTube Music itself.

### Requirements
    pip install yt_dlp mutagen ytmusicapi
You will also need ffmpeg installed in your system.

### Usage
    python youtubemusicdownloader.py "(link)"   (Support multiple entries)

Special thanks to Patrick Timm for helping me out in this project.

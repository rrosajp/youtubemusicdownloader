# YouTube Music Downloader
A simple Python script to download YouTube Music playlists, albums or tracks by providing a link.
By default, tracks are downloaded in AAC 128k codec (140), but you can get AAC 256k (141) if you place a YouTube Music Premium cookies.txt at the same directory as this script and Opus (251) by typing "opus" as the last argument.
Tags (album artist, album cover, album name, album track count, album year, track artist, track lyrics, track name, track number, track rating) are fetched from YouTube Music itself.

### Requirements
    pip3 install -r requirements.txt
You will also need ffmpeg installed in your system.

### Usage
    python youtubemusicdownloader.py "(link)"   (Support multiple entries)

Special thanks to Patrick Timm for helping me out in this project.

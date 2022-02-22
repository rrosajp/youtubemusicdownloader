# YouTube Music Downloader
A simple Python script to download YouTube Music playlists, albums or tracks by providing a link.
By default, tracks are downloaded in AAC 128k codec (140), but you can get AAC 256k (141) if you place a YouTube Music Premium cookies.txt at the same directory as this script and Opus (251) by using the flag "--o".
Tags (album artist, album cover, album name, album track count, album year, track artist, track lyrics, track name, track number, track rating) are fetched from YouTube Music itself.

### Requirements
    pip3 install -r requirements.txt
You will also need ffmpeg installed in your system.

### Usage
    python youtubemusicdownloader.py [-h] [--o] [--c C] [--e E] [--s] [--n] url [url ...]
    positional arguments:
      url                   Any valid YouTube Music album/playlist/track URL.

    options:
      -h, --help            show this help message and exit
      --o, --opus           Set track download format to Opus (251). Default is AAC (141/140).
      --c C, --coverresolution C
                            "max" or any valid number. Default is "1200".
      --e E, --excludetags E
                            Any valid tag ("album", "albumartist", "artist", "artwork", "lyrics", "rating", "totaltracks", "tracknumber", "tracktitle" and "year") separated by comma     
                            and without space.
      --s, --savecover      Save track album cover as "Cover.jpg" in track download directory.
      --n, --nodirectorystructure
                            Set track download directory to "/YouTube Music/Artist - Song.m4a/.opus".

Special thanks to Patrick Timm for helping me out in this project.

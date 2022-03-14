# YouTube Music Downloader
A simple Python script to download YouTube Music tacks by providing a link.
Tags are fetched from YouTube Music itself.

### Requirements
    pip3 install -r requirements.txt
You will also need ffmpeg installed in your system.

### Usage
    positional arguments:
      url                   Any valid YouTube Music URL.
    
    options:
      -h, --help            show this help message and exit
      --f F, --format F     141 (AAC 256kbps), 251 (Opus 160kbps) or 140 (AAC 128kbps). Requires a valid cookie file for
                            141. Default is 140.
      --e E, --excludetags E
                            Any valid tag ("album", "albumartist", "artist", "artwork", "lyrics", "rating", "totaltracks",
                            "tracknumber", "tracktitle" and "year") separated by comma with no spaces.
      --d, --downloadartwork
                            Download artwork as "Cover.jpg" in download directory.
      --a A, --artworksize A
                            "max" or any valid number. Default is "1200".

Special thanks to Patrick Timm for helping me out in this project.

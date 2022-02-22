from mutagen.mp4 import MP4, MP4Cover
import music_tag
import os
import platform
import requests
import yt_dlp
import argparse
import subprocess
import re
from ytmusicapi import YTMusic
ytmusic = YTMusic()

# Arguments.
parser = argparse.ArgumentParser(description="Download YouTube Music tracks.")
parser.add_argument("url", action="append",
                    help="Any valid YouTube Music album/playlist/track URL.", nargs="+")
parser.add_argument("--o", "--opus", action="store_true",
                    help="Set track download format to Opus (251). Default is AAC (141/140).")
parser.add_argument("--c", "--coverresolution",
                    help="\"max\" or any valid number. Default is \"1200\".")
parser.add_argument("--e", "--excludetags", help="Any valid tag (\"album\", \"albumartist\", \"artist\", \"artwork\", \"lyrics\", \"rating\", \"totaltracks\", \"tracknumber\", \"tracktitle\" and \"year\") separated by comma with no space.",  nargs=1)
parser.add_argument("--s", "--savecover", action="store_true",
                    help="Save track album cover as \"Cover.jpg\" in track download directory.")
parser.add_argument("--n", "--nodirectorystructure", action="store_true",
                    help="Set track download directory to \"/YouTube Music/Artist - Song.m4a/.opus\".")
args = parser.parse_args()
url_input = args.url[0]

# URL check.


def url_check(url):
    if re.search(r"watch\?v=\S\S\S\S\S\S\S\S\S\S\S", url) != None:
        track_video_id = re.search(
            r"watch\?v=\S\S\S\S\S\S\S\S\S\S\S", url).group(0)[8:]
        track_details = ytmusic.get_watch_playlist(track_video_id)
        track_video_details = ytmusic.get_song(track_video_id)
        track_details["tracks"][0]["album"]["id"]
        track_video_details["streamingData"]
        return [track_video_id]
    if re.search(r"playlist\?list=OLAK5uy_\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S", url) != None:
        album_playlist_id = re.search(
            r"playlist\?list=OLAK5uy_\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S", url).group(0)[14:]
        album_browse_id = ytmusic.get_album_browse_id(album_playlist_id)
        album_details = ytmusic.get_album(album_browse_id)
        ydl_opts = {"extract_flat": True, "skip_download": True,
                    "quiet": True, "no_warnings": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            album_playlist_details = ydl.extract_info(
                "https://music.youtube.com/playlist?list=" + album_playlist_id, download=False)
        track_video_id = []
        for a in range(len(album_playlist_details["entries"])):
            if album_details["tracks"][a]["videoId"] == None:
                pass
            else:
                track_video_id.append(
                    album_playlist_details["entries"][a]["id"])
        track_video_id[0]
        return track_video_id
    if re.search(r"playlist\?list=\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S", url) != None:
        playlist_id = re.search(
            r"playlist\?list=\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S", url).group(0)[14:]
        playlis_details = ytmusic.get_playlist(playlist_id)
        track_video_id = []
        for a in range(playlis_details["trackCount"]):
            try:
                playlis_details["tracks"][a]["album"]["id"]
                if playlis_details["tracks"][a]["videoId"] == None:
                    pass
                else:
                    track_video_id.append(
                        playlis_details["tracks"][a]["videoId"])
            except:
                pass
        track_video_id[0]
        return track_video_id
    raise

# Fetch tags.


def fetch_tags(track_video_id, cover_resolution):
    illegal_characters = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]
    track_details = ytmusic.get_watch_playlist(track_video_id)
    track_album_details = ytmusic.get_album(
        track_details["tracks"][0]["album"]["id"])
    track_album_artist = track_album_details["artists"][0]["name"]
    track_album_artist_fixed = track_album_artist
    if "w60-h60-s" in track_album_details["thumbnails"][0]["url"]:
        track_album_cover = requests.get(
            track_album_details["thumbnails"][0]["url"].replace("w60-h60-s", "w" + cover_resolution)).content
    else:
        track_album_cover = requests.get(
            track_album_details["thumbnails"][0]["url"].replace("w60-h60", "w" + cover_resolution)).content
    track_album_name = track_album_details["title"]
    track_album_name_fixed = track_album_name
    track_album_total_tracks = track_album_details["trackCount"]
    track_album_year = track_album_details["year"]
    track_artist = track_album_details["artists"][0]["name"]
    track_artist_fixed = track_album_details["artists"][0]["name"]
    try:
        track_lyrics_id = ytmusic.get_lyrics(track_details["lyrics"])
        track_lyrics = track_lyrics_id["lyrics"]
    except:
        track_lyrics = None
    ydl_opts = {"extract_flat": True, "skip_download": True,
                "quiet": True, "no_warnings": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        track_album_playlist_details = ydl.extract_info(
            "https://music.youtube.com/playlist?list=" + track_album_details["audioPlaylistId"], download=False)
    for a in range(len(track_album_playlist_details["entries"])):
        if track_album_playlist_details["entries"][a]["id"] == track_video_id:
            track_name = track_album_details["tracks"][a]["title"]
            track_name_fixed = track_name
            track_number = 1 + a
            track_number_fixed = "%02d" % (1 + a)
            if track_album_details["tracks"][a]["isExplicit"] == True:
                track_rating = 4
            else:
                track_rating = 0
    for a in range(len(illegal_characters)):
        track_album_artist_fixed = track_album_artist_fixed.replace(
            illegal_characters[a], "_")
        track_album_name_fixed = track_album_name_fixed.replace(
            illegal_characters[a], "_")
        track_artist_fixed = track_artist_fixed.replace(
            illegal_characters[a], "_")
        track_name_fixed = track_name_fixed.replace(illegal_characters[a], "_")
    if track_album_artist_fixed.endswith(".") == True:
        track_album_artist_fixed = track_album_artist_fixed.replace(".", "_")
    if track_album_name_fixed.endswith(".") == True:
        track_album_name_fixed = track_album_name_fixed.replace(".", "_")
    return {"trackAlbumArtist": track_album_artist,
            "trackAlbumArtistFixed": track_album_artist_fixed,
            "trackAlbumCover": track_album_cover,
            "trackAlbumName": track_album_name,
            "trackAlbumNameFixed": track_album_name_fixed,
            "trackAlbumTotalTracks": track_album_total_tracks,
            "trackAlbumYear": track_album_year,
            "trackArtist": track_artist,
            "trackArtistFixed": track_artist_fixed,
            "trackLyrics": track_lyrics,
            "trackName": track_name,
            "trackNameFixed": track_name_fixed,
            "trackNumber": track_number,
            "trackNumberFixed": track_number_fixed,
            "trackRating": track_rating,
            "trackVideoId": track_video_id
            }

# Get download preferences.


def get_download_preferences(opus, no_directory_structure, track_tags):
    if opus == True:
        download_extension = ".opus"
        download_format = "251"
    else:
        download_extension = ".m4a"
        download_format = "141/140"
    if platform.system() == "Windows":
        current_directory = "\\\\?\\" + os.getcwd()
        slash = "\\"
    else:
        current_directory = os.getcwd()
        slash = "/"
    if no_directory_structure == False:
        track_download_directory = current_directory + slash + "YouTube Music" + slash + \
            track_tags["trackAlbumArtistFixed"] + slash + track_tags["trackAlbumNameFixed"] + slash + \
            track_tags["trackNumberFixed"] + " " + \
            track_tags["trackNameFixed"] + download_extension
        cover_download_directory = current_directory + slash + "YouTube Music" + slash + \
            track_tags["trackAlbumArtistFixed"] + slash + \
            track_tags["trackAlbumNameFixed"] + slash
    else:
        track_download_directory = current_directory + slash + "YouTube Music" + slash + \
            track_tags["trackArtistFixed"] + " - " + \
            track_tags["trackNameFixed"] + download_extension
        cover_download_directory = current_directory + slash + "YouTube Music" + slash
    return {"trackDownloadDirectory": track_download_directory, "coverDownloadDirectory": cover_download_directory, "downloadFormat": download_format}

# Download tracks.


def download(download_preferences, track_tags):
    ydl_opts = {"format": download_preferences["downloadFormat"],
                "cookiefile": "cookies.txt",
                "outtmpl": download_preferences["trackDownloadDirectory"],
                "quiet": True,
                "no_warnings": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download("https://music.youtube.com/watch?v=" +
                     track_tags["trackVideoId"])
    if download_preferences["downloadFormat"] == "251":
        subprocess.check_output("ffmpeg -i \"" + download_preferences["trackDownloadDirectory"] +
                                "\" -f opus -c copy \"" + download_preferences["trackDownloadDirectory"] + ".temp\"")
        os.remove(download_preferences["trackDownloadDirectory"])
        os.rename(download_preferences["trackDownloadDirectory"] +
                  ".temp", download_preferences["trackDownloadDirectory"])

# Apply tags.


def apply_tags(download_preferences, exclude_tags, track_tags):
    if download_preferences["downloadFormat"] == "251":
        tags = music_tag.load_file(
            download_preferences["trackDownloadDirectory"])
        if exclude_tags["album"] != True:
            tags["album"] = track_tags["trackAlbumName"]
        if exclude_tags["albumartist"] != True:
            tags["albumartist"] = track_tags["trackAlbumArtist"]
        if exclude_tags["artist"] != True:
            tags["artist"] = track_tags["trackArtist"]
        if exclude_tags["artwork"] != True:
            tags["artwork"] = track_tags["trackAlbumCover"]
        if exclude_tags["lyrics"] != True:
            if track_tags["trackLyrics"] != None:
                tags["lyrics"] = track_tags["trackLyrics"]
        if exclude_tags["totaltracks"] != True:
            tags["totaltracks"] = track_tags["trackAlbumTotalTracks"]
        if exclude_tags["tracknumber"] != True:
            tags["tracknumber"] = track_tags["trackNumber"]
        if exclude_tags["tracktitle"] != True:
            tags["tracktitle"] = track_tags["trackName"]
        if exclude_tags["year"] != True:
            tags["year"] = track_tags["trackAlbumYear"]
        if exclude_tags["all"] != True:
            tags.save()
    else:
        tags = MP4(download_preferences["trackDownloadDirectory"]).tags
        if exclude_tags["album"] != True:
            tags["\xa9alb"] = track_tags["trackAlbumName"]
        if exclude_tags["albumartist"] != True:
            tags["aART"] = track_tags["trackAlbumArtist"]
        if exclude_tags["artist"] != True:
            tags["\xa9ART"] = track_tags["trackArtist"]
        if exclude_tags["artwork"] != True:
            tags["covr"] = [
                MP4Cover(track_tags["trackAlbumCover"], imageformat=MP4Cover.FORMAT_JPEG)]
        if exclude_tags["lyrics"] != True:
            if track_tags["trackLyrics"] != None:
                tags["\xa9lyr"] = track_tags["trackLyrics"]
        if exclude_tags["tracktitle"] != True:
            tags["\xa9nam"] = track_tags["trackName"]
        if exclude_tags["totaltracks"] != True:
            tags["trkn"] = [(0, track_tags["trackAlbumTotalTracks"])]
            if exclude_tags["tracknumber"] != True:
                tags["trkn"] = [(track_tags["trackNumber"],
                                 track_tags["trackAlbumTotalTracks"])]
        if exclude_tags["tracknumber"] != True:
            tags["trkn"] = [(track_tags["trackNumber"], 0)]
            if exclude_tags["totaltracks"] != True:
                tags["trkn"] = [(track_tags["trackNumber"],
                                 track_tags["trackAlbumTotalTracks"])]
        if exclude_tags["rating"] != True:
            tags["rtng"] = [track_tags["trackRating"]]
        if exclude_tags["year"] != True:
            tags["\xa9day"] = track_tags["trackAlbumYear"]
        if exclude_tags["all"] != True:
            tags.save(download_preferences["trackDownloadDirectory"])

# Download cover.


def save_cover(save_cover, download_preferences, track_tags):
    if save_cover == True:
        with open(download_preferences["coverDownloadDirectory"] + "Cover.jpg", 'wb') as cover_file:
            cover_file.write(track_tags["trackAlbumCover"])


# Set cover size.
if args.c != "max":
    try:
        if (int(args.c) < 0) or (int(args.c) > 16383):
            cover_resolution = "1200"
        else:
            cover_resolution = args.c
    except:
        cover_resolution = "1200"
else:
    cover_resolution = "16383"

# Set exlcude tags.
exclude_tags = {"album": False,
                "albumartist": False,
                "artist": False,
                "artwork": False,
                "lyrics": False,
                "rating": False,
                "totaltracks": False,
                "tracknumber": False,
                "tracktitle": False,
                "year": False,
                "all": False}
if args.e != None:
    exclude_tags_preferences = args.e[0].split(",")
    for a in range(len(exclude_tags_preferences)):
        exclude_tags[exclude_tags_preferences[a]] = True

# Start download.
track_video_id = []
print("Checking URL input...")
for a in range(len(url_input)):
    try:
        track_video_id += (url_check(url_input[a]))
    except KeyboardInterrupt:
        exit()
    except:
        pass
try:
    track_video_id[0]
except:
    exit("No valid link input provided.")
for a in range(len(track_video_id)):
    try:
        print("Fetching tags (Track " + str(a + 1) +
              " of " + str(len(track_video_id)) + ")...")
        track_tags = fetch_tags(track_video_id[a], cover_resolution)
        download_preferences = get_download_preferences(
            args.o, args.n, track_tags)
        print("Downloading " + "\"" + track_tags["trackName"] + "\"" + "...")
        download(download_preferences, track_tags)
        apply_tags(download_preferences, exclude_tags, track_tags)
        save_cover(args.s, download_preferences, track_tags)
        print("Download finished!")
    except KeyboardInterrupt:
        exit()
    except:
        print("Download failed (Track " + str(a + 1) +
              " of " + str(len(track_video_id)) + ").")
exit("All done.")

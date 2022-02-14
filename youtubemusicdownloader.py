import sys
import platform
import os
from ytmusicapi import YTMusic
import re
import yt_dlp
from urllib.request import urlopen
from mutagen.mp4 import MP4, MP4Cover

linkInput = sys.argv

# Get current directory.
if platform.system() == "Windows":
    currentDirectory = "\\\\?\\" + os.getcwd()
    slash = "\\"
else:
    currentDirectory = os.getcwd()
    slash = "/"

# Stop if no link inputs are provided.
if len(linkInput) == 1:
    exit("Please enter at least one link to continue.")

del linkInput[0]

ytmusic = YTMusic()

# Link input check.


def linkInputCheck(link):
    if re.search(r"watch\?v=\S\S\S\S\S\S\S\S\S\S\S", link) != None:
        trackVideoId = re.search(
            r"watch\?v=\S\S\S\S\S\S\S\S\S\S\S", link).group(0)[8:]
        trackDetails = ytmusic.get_watch_playlist(trackVideoId)
        trackVideoDetails = ytmusic.get_song(trackVideoId)
        trackDetails["tracks"][0]["album"]["id"]
        trackVideoDetails["streamingData"]
        return [trackVideoId]
    if re.search(r"playlist\?list=OLAK5uy_\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S", link) != None:
        albumPlaylistId = re.search(
            r"playlist\?list=OLAK5uy_\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S", link).group(0)[14:]
        albumBrowseId = ytmusic.get_album_browse_id(albumPlaylistId)
        albumDetails = ytmusic.get_album(albumBrowseId)
        ydl_opts = {"extract_flat": True, "skip_download": True,
                    "quiet": True, "no_warnings": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            albumPlaylistDetails = ydl.extract_info(
                "https://music.youtube.com/playlist?list=" + albumPlaylistId, download=False)
        trackVideoId = []
        for a in range(len(albumPlaylistDetails["entries"])):
            if albumDetails["tracks"][a]["videoId"] == None:
                pass
            else:
                trackVideoId.append(albumPlaylistDetails["entries"][a]["id"])
        trackVideoId[0]
        return trackVideoId
    if re.search(r"playlist\?list=\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S", link) != None:
        playlistId = re.search(
            r"playlist\?list=\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S", link).group(0)[14:]
        playlistDetails = ytmusic.get_playlist(playlistId)
        trackVideoId = []
        for a in range(playlistDetails["trackCount"]):
            try:
                playlistDetails["tracks"][a]["album"]["id"]
                if playlistDetails["tracks"][a]["videoId"] == None:
                    pass
                else:
                    trackVideoId.append(
                        playlistDetails["tracks"][a]["videoId"])
            except:
                pass
        trackVideoId[0]
        return trackVideoId
    raise

# Fetch trackTags.


def fetchTags(trackVideoId):
    trackWatchList = ytmusic.get_watch_playlist(trackVideoId)
    trackAlbumDetails = ytmusic.get_album(
        trackWatchList["tracks"][0]["album"]["id"])
    trackAlbumName = trackAlbumDetails["title"]
    trackAlbumYear = trackAlbumDetails["year"]
    trackAlbumTotalTracks = trackAlbumDetails["trackCount"]
    trackAlbumArtist = trackAlbumDetails["artists"][0]["name"]
    trackAlbumCover = urlopen(
        trackAlbumDetails["thumbnails"][0]["url"].replace("w60-h60", "w1200-h1200"))
    trackArtist = trackWatchList["tracks"][0]["artists"][0]["name"]
    try:
        trackLyricsId = ytmusic.get_lyrics(trackWatchList["lyrics"])
        trackLyrics = trackLyricsId["lyrics"]
    except:
        trackLyrics = None
    ydl_opts = {"extract_flat": True, "skip_download": True,
                "quiet": True, "no_warnings": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        trackAlbumPlaylistDetails = ydl.extract_info(
            "https://music.youtube.com/playlist?list=" + trackAlbumDetails["audioPlaylistId"], download=False)
    for a in range(len(trackAlbumPlaylistDetails["entries"])):
        if trackAlbumPlaylistDetails["entries"][a]["id"] == trackVideoId:
            trackNumber = 1 + a
            trackNumberFixed = "%02d" % (1 + a)
            trackName = trackAlbumDetails["tracks"][a]["title"]
            if trackAlbumDetails["tracks"][a]["isExplicit"] == True:
                trackRating = 4
            else:
                trackRating = 0
    trackNameFixed = trackName
    trackAlbumNameFixed = trackAlbumName
    trackAlbumArtistFixed = trackAlbumArtist
    illegalCharacters = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]
    for a in range(len(illegalCharacters)):
        trackNameFixed = trackNameFixed.replace(illegalCharacters[a], "_")
        trackAlbumNameFixed = trackAlbumNameFixed.replace(
            illegalCharacters[a], "_")
        trackAlbumArtistFixed = trackAlbumArtistFixed.replace(
            illegalCharacters[a], "_")
    if trackAlbumNameFixed.endswith(".") == True:
        trackAlbumNameFixed = trackAlbumNameFixed.replace(".", "_")
    if trackAlbumArtistFixed.endswith(".") == True:
        trackAlbumArtistFixed = trackAlbumArtistFixed.replace(".", "_")
    return {"trackVideoId": trackVideoId, "trackAlbumName": trackAlbumName, "trackAlbumYear": trackAlbumYear, "trackAlbumTotalTracks": trackAlbumTotalTracks,
            "trackAlbumArtist": trackAlbumArtist, "trackAlbumCover": trackAlbumCover, "trackArtist": trackArtist, "trackLyrics": trackLyrics, "trackNumber": trackNumber, "trackNumberFixed": trackNumberFixed,
            "trackName": trackName, "trackRating": trackRating, "trackNameFixed": trackNameFixed, "trackAlbumNameFixed": trackAlbumNameFixed, "trackAlbumArtistFixed": trackAlbumArtistFixed}

# Download tracks.


def download(trackTags):
    ydl_opts = {'format': '141/140',
                'cookiefile': "cookies.txt",
                'outtmpl': currentDirectory + slash + "YouTube Music" + slash + trackTags["trackAlbumArtistFixed"] + slash + trackTags["trackAlbumNameFixed"] + slash + trackTags["trackNumberFixed"] + " " + trackTags["trackNameFixed"] + ".m4a", 'quiet': True, "no_warnings": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download('https://music.youtube.com/watch?v=' +
                     trackTags["trackVideoId"])

# Tag files.


def applyTags(trackTags):
    file = MP4(currentDirectory + slash + "YouTube Music" + slash +
               trackTags["trackAlbumArtistFixed"] + slash + trackTags["trackAlbumNameFixed"] + slash + trackTags["trackNumberFixed"] + " " + trackTags["trackNameFixed"] + ".m4a").tags
    file['\xa9nam'] = trackTags["trackName"]
    file['\xa9alb'] = trackTags["trackAlbumName"]
    file['aART'] = trackTags["trackAlbumArtist"]
    file['\xa9day'] = trackTags["trackAlbumYear"]
    file['\xa9ART'] = trackTags["trackArtist"]
    file['trkn'] = [
        (trackTags["trackNumber"], trackTags["trackAlbumTotalTracks"])]
    file['rtng'] = [trackTags["trackRating"]]
    file["covr"] = [
        MP4Cover(trackTags["trackAlbumCover"].read(), imageformat=MP4Cover.FORMAT_JPEG)]
    if trackTags["trackLyrics"] != None:
        file['\xa9lyr'] = trackTags["trackLyrics"]
    file.save(currentDirectory + slash + "YouTube Music" + slash +
              trackTags["trackAlbumArtistFixed"] + slash + trackTags["trackAlbumNameFixed"] + slash + trackTags["trackNumberFixed"] + " " + trackTags["trackNameFixed"] + ".m4a")


# Check input.
trackVideoId = []
print("Checking link input...")
for a in range(len(linkInput)):
    try:
        trackVideoId += (linkInputCheck(linkInput[a]))
    except KeyboardInterrupt:
        exit()
    except:
        pass
try:
    trackVideoId[0]
except:
    exit("No valid link input provided.")

# Start downloading.
for a in range(len(trackVideoId)):
    print("Fetching tags (Track " + str(a + 1) +
          " of " + str(len(trackVideoId)) + ")...")
    trackTags = fetchTags(trackVideoId[a])
    print("Downloading " + "\"" + trackTags["trackName"] + "\"" + "...")
    download(trackTags)
    applyTags(trackTags)
    print("Done!")

exit()

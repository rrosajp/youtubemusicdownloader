import sys
from ytmusicapi import YTMusic
import re
import yt_dlp
import platform
import os
import requests
import music_tag
from mutagen.mp4 import MP4, MP4Cover

linkInput = sys.argv

ytmusic = YTMusic()

# Stop if no link inputs are provided.
if len(linkInput) == 1:
    exit("Please enter at least one link to continue.")

del linkInput[0]

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

# Get download options:


def getDownloadOptions():
    if linkInput[-1] == "opus":
        return {"format": "251", "extension": ".webm"}
    else:
        return {"format": "141/140", "extension": ".m4a"}

# Fetch trackTags.


def fetchTags(trackVideoId):
    trackWatchList = ytmusic.get_watch_playlist(trackVideoId)
    trackAlbumDetails = ytmusic.get_album(
        trackWatchList["tracks"][0]["album"]["id"])
    trackAlbumName = trackAlbumDetails["title"]
    trackAlbumYear = trackAlbumDetails["year"]
    trackAlbumTotalTracks = trackAlbumDetails["trackCount"]
    trackAlbumArtist = trackAlbumDetails["artists"][0]["name"]
    trackAlbumCover = requests.get(
        trackAlbumDetails["thumbnails"][0]["url"].replace("w60-h60", "w1200-h1200")).content
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

# Get output template.


def getDownloadDirectory(trackTags, downloadOptions):
    if platform.system() == "Windows":
        currentDirectory = "\\\\?\\" + os.getcwd()
        slash = "\\"
    else:
        currentDirectory = os.getcwd()
        slash = "/"
    downloadDirectory = currentDirectory + slash + "YouTube Music" + slash + \
        trackTags["trackAlbumArtistFixed"] + slash + trackTags["trackAlbumNameFixed"] + slash + \
        trackTags["trackNumberFixed"] + " " + \
        trackTags["trackNameFixed"] + downloadOptions["extension"]
    return downloadDirectory


# Download tracks.


def download(downloadOptions, downloadDirectory):
    ydl_opts = {"format": downloadOptions["format"],
                "cookiefile": "cookies.txt",
                "outtmpl": downloadDirectory,
                "quiet": True,
                "no_warnings": True}
    if downloadOptions["format"] == "251":
        ydl_opts["postprocessors"] = [{
            'key': 'FFmpegExtractAudio',
        }]
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download("https://music.youtube.com/watch?v=" +
                     trackTags["trackVideoId"])
    if downloadOptions["format"] == "251":
        os.rename(downloadDirectory[:-4] + "opus",
                  downloadDirectory[:-4] + "ogg",)

# Tag files.


def applyTags(downloadOptions, downloadDirectory, trackTags):
    if downloadOptions["format"] == "251":
        tags = music_tag.load_file(downloadDirectory[:-4] + "ogg")
        tags["album"] = trackTags["trackAlbumName"]
        tags["albumartist"] = trackTags["trackAlbumArtist"]
        tags["artist"] = trackTags["trackArtist"]
        tags["artwork"] = trackTags["trackAlbumCover"]
        if trackTags["trackLyrics"] != None:
            tags["lyrics"] = trackTags["trackLyrics"]
        tags["totaltracks"] = trackTags["trackAlbumTotalTracks"]
        tags["tracknumber"] = trackTags["trackNumber"]
        tags["tracktitle"] = trackTags["trackName"]
        tags["year"] = trackTags["trackAlbumYear"]
        tags.save()
    else:
        tags = MP4(downloadDirectory).tags
        tags["\xa9nam"] = trackTags["trackName"]
        tags["\xa9alb"] = trackTags["trackAlbumName"]
        tags["aART"] = trackTags["trackAlbumArtist"]
        tags["\xa9day"] = trackTags["trackAlbumYear"]
        tags["\xa9ART"] = trackTags["trackArtist"]
        tags["trkn"] = [
            (trackTags["trackNumber"], trackTags["trackAlbumTotalTracks"])]
        tags["rtng"] = [trackTags["trackRating"]]
        tags["covr"] = [
            MP4Cover(trackTags["trackAlbumCover"], imageformat=MP4Cover.FORMAT_JPEG)]
        if trackTags["trackLyrics"] != None:
            tags["\xa9lyr"] = trackTags["trackLyrics"]
        tags.save(downloadDirectory)


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
downloadOptions = getDownloadOptions()
for a in range(len(trackVideoId)):
    try:
        print("Fetching tags (Track " + str(a + 1) +
              " of " + str(len(trackVideoId)) + ")...")
        trackTags = fetchTags(trackVideoId[a])
        downloadDirectory = getDownloadDirectory(trackTags, downloadOptions)
        print("Downloading " + "\"" + trackTags["trackName"] + "\"" + "...")
        download(downloadOptions, downloadDirectory)
        applyTags(downloadOptions, downloadDirectory, trackTags)
        print("Done!")
    except KeyboardInterrupt:
        break
    except:
        print("Failed to download (Track " + str(a + 1) +
              " of " + str(len(trackVideoId)) + ").")
        pass

exit()

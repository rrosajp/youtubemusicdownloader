import sys
import platform
import os
from ytmusicapi import YTMusic
import re
import yt_dlp
import urllib.request
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
    print("Please enter at least one link to continue.")
    exit()

del linkInput[0]

ytmusic = YTMusic()

# Link input check.
def linkInputCheck(link):

    if re.search(r"watch\?v=\S\S\S\S\S\S\S\S\S\S\S", link) != None:
        trackVideoId = re.search(r"watch\?v=\S\S\S\S\S\S\S\S\S\S\S", link).group(0)[8:]
        try:
            trackDetails = ytmusic.get_watch_playlist(trackVideoId)
            trackVideoDetails = ytmusic.get_song(trackVideoId)
            trackDetails["tracks"][0]["album"]["id"]
            if trackVideoDetails["playabilityStatus"]["status"] == "UNPLAYABLE":
                return [False]
            return [trackVideoId]
        except:
            return [False]
        return [False]

    if re.search(r"playlist\?list=OLAK5uy_\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S", link) != None:
        albumPlaylistId = re.search(r"playlist\?list=OLAK5uy_\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S", link).group(0)[14:]
        albumBrowseId = ytmusic.get_album_browse_id(albumPlaylistId)
        if albumBrowseId != None:
            albumDetails = ytmusic.get_album(albumBrowseId)
            ydl_opts = {"extract_flat": True, "skip_download": True, "quiet": True, "no_warnings": True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                albumPlaylistDetails = ydl.extract_info("https://music.youtube.com/playlist?list=" + albumPlaylistId, download=False)
            trackVideoId = []
            for a in range(len(albumPlaylistDetails["entries"])):
                if albumDetails["tracks"][a]["videoId"] == None:
                    pass
                else:
                    trackVideoId.append(albumPlaylistDetails["entries"][a]["id"])
            if trackVideoId == []:
                return [False]
            return trackVideoId
        return [False]

    if re.search(r"playlist\?list=\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S", link) != None:
        playlistId = re.search(r"playlist\?list=\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S", link).group(0)[14:]
        try:
            playlistDetails = ytmusic.get_playlist(playlistId)
        except:
            return [False]
        trackVideoId = []
        for a in range(playlistDetails["trackCount"]):
            try:
                playlistDetails["tracks"][a]["album"]["id"]
                if playlistDetails["tracks"][a]["videoId"] == None:
                    pass
                else:
                    trackVideoId.append(playlistDetails["tracks"][a]["videoId"])
            except:
                pass
        if trackVideoId == []:
            return [False]
        return trackVideoId
    return [False]

# Start checking.
trackVideoIdWithFalseResults = []
print("Checking link input...")
for a in range(len(linkInput)):
    trackVideoIdWithFalseResults += (linkInputCheck(linkInput[a]))

# Remove falses.
trackVideoId = []
for a in range(len(trackVideoIdWithFalseResults)):
    if trackVideoIdWithFalseResults[a] != False:
        trackVideoId.append(trackVideoIdWithFalseResults[a])

# Stop if all link inputs are invalid.
if trackVideoId == []:
    print("No valid link input provided.")
    exit()

# Fetch tags
for a in range(len(trackVideoId)):
    print("Fetching tags (Track " + str(a + 1) + " of " + str(len(trackVideoId)) + ")...")
    trackWatchList = ytmusic.get_watch_playlist(trackVideoId[a])
    albumDetails = ytmusic.get_album(trackWatchList["tracks"][0]["album"]["id"])
    albumName = albumDetails["title"]
    albumYear = albumDetails["year"]
    albumTotalTracks = albumDetails["trackCount"]
    albumArtist = albumDetails["artists"][0]["name"]
    albumCoverUrl = albumDetails["thumbnails"][0]["url"].replace("w60-h60", "w1200-h1200")
    trackArtist = trackWatchList["tracks"][0]["artists"][0]["name"]
    try:
        trackLyricsId = ytmusic.get_lyrics(trackWatchList["lyrics"])
        trackLyrics = trackLyricsId["lyrics"]
    except:
        trackLyrics = None
    ydl_opts = {"extract_flat": True, "skip_download": True, "quiet": True, "no_warnings": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        albumPlaylistDetails = ydl.extract_info("https://music.youtube.com/playlist?list=" + albumDetails["audioPlaylistId"], download=False)
    for b in range(len(albumPlaylistDetails["entries"])):
        if albumPlaylistDetails["entries"][b]["id"] == trackVideoId[a]:
            trackNumber = 1 + b
            trackNumberFixed = "%02d" % (1 + b)
            trackName = albumDetails["tracks"][b]["title"]
            if albumDetails["tracks"][b]["isExplicit"] == True:
                trackRating = 4
            else:
                trackRating = 0

    # Remove illegal characters
    trackNameFixed = trackName
    albumNameFixed = albumName
    albumArtistFixed = albumArtist
    illegalCharacters = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]
    for c in range(len(illegalCharacters)):
        trackNameFixed = trackNameFixed.replace(illegalCharacters[c], "_")
        albumNameFixed = albumNameFixed.replace(illegalCharacters[c], "_")
        albumArtistFixed = albumArtistFixed.replace(illegalCharacters[c], "_")
    if albumNameFixed.endswith(".") == True:
        albumNameFixed = albumNameFixed.replace(".", "_")
    if albumArtistFixed.endswith(".") == True:
        albumArtistFixed = albumArtistFixed.replace(".", "_")

    # Start downloading.
    print("Downloading " + "\"" + trackName + "\"" + "...")
    try:
        downloadDirectory = currentDirectory + slash + "YouTube Music" + slash + albumArtistFixed + slash + albumNameFixed + slash
        ydl_opts = {'format': '141/140', 'cookiefile': "cookies.txt", 'outtmpl': downloadDirectory + trackNumberFixed + " " + trackNameFixed + ".m4a", 'quiet': True,"no_warnings": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download('https://music.youtube.com/watch?v=' + trackVideoId[a])
        if os.path.exists(downloadDirectory + "Cover.jpg") == False:
            urllib.request.urlretrieve(albumCoverUrl, downloadDirectory + "Cover.jpg")
        tags = MP4(downloadDirectory + trackNumberFixed + " " + trackNameFixed + ".m4a").tags
        tags['\xa9nam'] = trackName
        tags['\xa9alb'] = albumName
        tags['aART'] = albumArtist
        tags['\xa9day'] = albumYear
        tags['\xa9ART'] = trackArtist
        tags['trkn'] = [(trackNumber, albumTotalTracks)]
        tags['rtng'] = [trackRating]
        with open(downloadDirectory + "Cover.jpg", "rb") as cover:
            tags["covr"] = [MP4Cover(cover.read(), imageformat=MP4Cover.FORMAT_JPEG)]
        if trackLyrics != None:
            tags['\xa9lyr'] = trackLyrics
        tags.save(downloadDirectory + trackNumberFixed + " " + trackNameFixed + ".m4a")
    except KeyboardInterrupt:
        exit()
    except:
        print("Failed to download " + "\"" + trackName + "\"" + ".")
    print("Done!")
exit()

from logging import exception
from ytmusicapi import YTMusic
import yt_dlp
from mutagen.mp4 import MP4, MP4Cover
import urllib.request
import os
import re

ytmusic = YTMusic()

# link check
def albumLinkCheck(link):
    if re.search(r"watch\?v=\S\S\S\S\S\S\S\S\S\S\S", link) != None:
        videoId = re.search(r"watch\?v=\S\S\S\S\S\S\S\S\S\S\S", link).group(0)[8:]
        trackInfo = ytmusic.get_watch_playlist(videoId)
        try:
            return [True, "trackDownload", videoId, trackInfo["tracks"][0]["album"]["id"], trackInfo["tracks"][0]["artists"][0]["name"], trackInfo["lyrics"]]
        except:
            return [False]

    if re.search(r"playlist\?list=OLAK5uy_\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S", link) != None:
        albumPlaylistId = re.search(r"playlist\?list=OLAK5uy_\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S", link).group(0)[14:]
        albumBrowseId = ytmusic.get_album_browse_id(albumPlaylistId)
        if albumBrowseId is None:
            return [False]
        return [True, "albumDownload", albumBrowseId]

    if re.search(r"playlist\?list=\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S", link) != None:
        playlistId = re.search(r"playlist\?list=\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S", link).group(0)[14:]
        try: 
            playlistInfo = ytmusic.get_playlist(playlistId)
        except:
            return [False]
        albumBrowseId = []
        trackId = []
        trackArtist = []
        for i in range(playlistInfo["trackCount"]):
            try:
                albumBrowseId.append(playlistInfo["tracks"][i]["album"]["id"])
                trackId.append(playlistInfo["tracks"][i]["videoId"])
                trackArtist.append(playlistInfo["tracks"][i]["artists"][0]["name"])
                trackName.append(playlistInfo["tracks"][i]["title"])
            except:
                pass
        if albumBrowseId == []:
            return [False]
        return [True, "playlistDownload", albumBrowseId, trackId, trackArtist]
    return [False]

# ask user input
linkInput = input("Enter a YouTube Music album link, playlist link or track link: ")
downloadDetails = albumLinkCheck(linkInput)

# display errors
while downloadDetails[0] is False:
    linkInput = input("Invalid input. Enter a YouTube Music album link, playlist link or track link: ")
    downloadDetails = albumLinkCheck(linkInput)
print("Fetching tags...")

albumInfo = []
albumPlaylistDetails = []
albumTotalTracks = []
albumName = []
albumNameFixed = []
albumYear = []
albumTotalTracks = []
albumArtist = []
albumArtistFixed = []
albumCoverUrl = []
trackArtist = []
trackNumber = []
trackNumberFixed = []
trackName = []
trackNameFixed = []
trackVideoId = []
trackLyrics = []
trackWatchList = []
foundTrackNumber = 0

# fectch tags for single track
if downloadDetails[1] == 'trackDownload':
    albumInfo = ytmusic.get_album(downloadDetails[3])
    albumName = [albumInfo["title"]]
    albumNameFixed = [albumInfo["title"]]
    albumYear = [albumInfo["year"]]
    albumTotalTracks = [albumInfo["trackCount"]]
    albumArtist = [albumInfo["artists"][0]["name"]]
    albumArtistFixed = [albumInfo["artists"][0]["name"]]
    albumCoverUrl = [albumInfo["thumbnails"][0]["url"].replace("w60-h60", "w1200-h1200")]
    trackArtist = [downloadDetails[4]]
    trackVideoId = [downloadDetails[2]]
    ydl_opts = {
    "extract_flat": True,
    "skip_download": True,
    "quiet": True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlistInfo = ydl.extract_info("https://music.youtube.com/playlist?list=" + albumInfo["audioPlaylistId"], download=False)
    for i in range(len(playlistInfo["entries"])):
        if playlistInfo["entries"][i]["id"] == downloadDetails[2]:
            trackNumber = [1 + i]
            trackNumberFixed = ["%02d" % (i + 1)]
            trackName = [albumInfo["tracks"][i]["title"]]
            trackNameFixed = [albumInfo["tracks"][i]["title"]]
            break
    try:
        trackLyricsId = ytmusic.get_lyrics(downloadDetails[5])
        trackLyrics = [trackLyricsId["lyrics"]]
    except:
        trackLyrics = [None]
    
# fetch tags for album
if downloadDetails[1] == "albumDownload":
    albumInfo = ytmusic.get_album(downloadDetails[2])
    for i in range(albumInfo["trackCount"]):
        albumName.append(albumInfo["title"])
        albumNameFixed.append(albumInfo["title"])
        albumYear.append(albumInfo["year"])
        albumTotalTracks.append(albumInfo["trackCount"])
        albumArtist.append(albumInfo["artists"][0]["name"])
        albumArtistFixed.append(albumInfo["artists"][0]["name"])
        albumCoverUrl.append(albumInfo["thumbnails"][0]["url"].replace("w60-h60", "w1200-h1200"))
        if albumInfo['tracks'][i]['artists'] == None:
            trackArtist.append(albumInfo['artists'][0]['name'])
        else:
            trackArtist.append(albumInfo['tracks'][i]['artists'][0]['name'])
        trackNumber.append(i + 1)
        trackNumberFixed.append("%02d" % (i + 1))
        trackName.append(albumInfo["tracks"][i]["title"])
        trackNameFixed.append(albumInfo["tracks"][i]["title"])

    ydl_opts = {
    "extract_flat": True,
    "skip_download": True,
    "quiet": True,
    "no_warnings": True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlistInfo = ydl.extract_info("https://music.youtube.com/playlist?list=" + albumInfo["audioPlaylistId"], download=False)
    for i in range(len(playlistInfo["entries"])):
        trackVideoId.append(playlistInfo["entries"][i]["id"])
    for i in range(len(trackVideoId)):
        trackWatchList = ytmusic.get_watch_playlist(trackVideoId[i])
        trackLyricsId = trackWatchList["lyrics"]
        if trackLyricsId == None:
            trackLyrics.append(None)
        else:
            trackLyricsInfo = ytmusic.get_lyrics(trackLyricsId)
            trackLyrics.append(trackLyricsInfo["lyrics"])

# fetch tags for playlist
if downloadDetails[1] == 'playlistDownload':
    for i in range(len(downloadDetails[2])):
        albumInfo.append(ytmusic.get_album(downloadDetails[2][i]))
        albumName.append(albumInfo[i]["title"])
        albumNameFixed.append(albumInfo[i]["title"])
        albumYear.append(albumInfo[i]["year"])
        albumTotalTracks.append(albumInfo[i]["trackCount"])
        albumArtist.append(albumInfo[i]["artists"][0]["name"])
        albumArtistFixed.append(albumInfo[i]["artists"][0]["name"])
        albumCoverUrl.append(albumInfo[i]["thumbnails"][0]["url"].replace("w60-h60", "w1200-h1200"))
        trackVideoId.append(downloadDetails[3][i])
        trackArtist.append(downloadDetails[4][i])
        ydl_opts = {
        "extract_flat": True,
        "skip_download": True,
        "quiet": True,
        "no_warnings": True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            albumPlaylistDetails.append(ydl.extract_info("https://music.youtube.com/playlist?list=" + albumInfo[i]["audioPlaylistId"], download=False))
        for j in range(len(albumPlaylistDetails[i]["entries"])):
            if albumPlaylistDetails[i]["entries"][j]["id"] == trackVideoId[i]:
                trackName.append(albumPlaylistDetails[i]["entries"][j]["title"])
                trackNameFixed.append(albumPlaylistDetails[i]["entries"][j]["title"])
                trackNumber.append(j + 1)
                trackNumberFixed.append("%02d" % (j + 1))
    for i in range(len(trackVideoId)):
        trackWatchList = ytmusic.get_watch_playlist(trackVideoId[i])
        trackLyricsId = trackWatchList["lyrics"]
        if trackLyricsId == None:
            trackLyrics.append(None)
        else:
            trackLyricsInfo = ytmusic.get_lyrics(trackLyricsId)
            trackLyrics.append(trackLyricsInfo["lyrics"])

# remove illegal characters
for i in range(len(trackName)):
    trackNameFixed[i] = trackNameFixed[i].replace('\\', '_')
    trackNameFixed[i] = trackNameFixed[i].replace('/', '_')
    trackNameFixed[i] = trackNameFixed[i].replace(':', '_')
    trackNameFixed[i] = trackNameFixed[i].replace('*', '_')
    trackNameFixed[i] = trackNameFixed[i].replace('?', '_')
    trackNameFixed[i] = trackNameFixed[i].replace('"', '_')
    trackNameFixed[i] = trackNameFixed[i].replace('<', '_')
    trackNameFixed[i] = trackNameFixed[i].replace('>', '_')
    trackNameFixed[i] = trackNameFixed[i].replace('|', '_')
    if trackNameFixed[i].endswith(".") == True:
        trackNameFixed[i] = trackNameFixed[i].replace('.', '_')


for i in range(len(albumArtist)):
    albumArtistFixed[i] = albumArtistFixed[i].replace('\\', '_')
    albumArtistFixed[i] = albumArtistFixed[i].replace('/', '_')
    albumArtistFixed[i] = albumArtistFixed[i].replace(':', '_')
    albumArtistFixed[i] = albumArtistFixed[i].replace('*', '_')
    albumArtistFixed[i] = albumArtistFixed[i].replace('?', '_')
    albumArtistFixed[i] = albumArtistFixed[i].replace('"', '_')
    albumArtistFixed[i] = albumArtistFixed[i].replace('<', '_')
    albumArtistFixed[i] = albumArtistFixed[i].replace('>', '_')
    albumArtistFixed[i] = albumArtistFixed[i].replace('|', '_')
    if albumArtistFixed[i].endswith(".") == True:
        albumArtistFixed[i] = albumArtistFixed[i].replace('.', '_')

for i in range(len(albumName)):
    albumNameFixed[i] = albumNameFixed[i].replace('\\', '_')
    albumNameFixed[i] = albumNameFixed[i].replace('/', '_')
    albumNameFixed[i] = albumNameFixed[i].replace(':', '_')
    albumNameFixed[i] = albumNameFixed[i].replace('*', '_')
    albumNameFixed[i] = albumNameFixed[i].replace('?', '_')
    albumNameFixed[i] = albumNameFixed[i].replace('"', '_')
    albumNameFixed[i] = albumNameFixed[i].replace('<', '_')
    albumNameFixed[i] = albumNameFixed[i].replace('>', '_')
    albumNameFixed[i] = albumNameFixed[i].replace('|', '_')
    if albumNameFixed[i].endswith(".") == True:
        albumNameFixed[i] = albumNameFixed[i].replace('.', '_')

# start downloading
for i in range(len(trackName)):
    try:
        print("Downloading " + trackName[i] + " (Track " + str(i + 1) + " of " + str(len(trackName)) + ")...")
        print(albumNameFixed[i])
        urllib.request.urlretrieve(albumCoverUrl[i], 'Cover.jpg')
        ydl_opts = {
            'format': '141/140',
            'cookiefile': 'cookies.txt',
            'outtmpl': 'YouTube Music/' + albumArtistFixed[i] + '/' + albumNameFixed[i] + '/' + str(trackNumberFixed[i]) + ' ' + trackNameFixed[i] + '.m4a',
            'quiet': True,
            "no_warnings": True
            }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download('https://music.youtube.com/watch?v=' + trackVideoId[i])
        tags = MP4('YouTube Music/' + albumArtistFixed[i] + '/' + albumNameFixed[i] + '/' + str(trackNumberFixed[i]) + ' ' + trackNameFixed[i] + '.m4a').tags
        tags['\xa9nam'] = trackName[i]
        tags['\xa9alb'] = albumName[i]
        tags['aART'] = albumArtist[i]
        tags['\xa9day'] = albumYear[i]
        tags['\xa9ART'] = trackArtist[i]
        tags['trkn'] = [(trackNumber[i], albumTotalTracks[i])]
        with open('Cover.jpg', "rb") as cover:
            tags["covr"] = [
            MP4Cover(cover.read(), imageformat=MP4Cover.FORMAT_JPEG)
            ]
        if trackLyrics[i] != None:
            tags['\xa9lyr'] = trackLyrics[i]
        tags.save('YouTube Music/' + albumArtistFixed[i] + '/' + albumNameFixed[i] + '/' + str(trackNumberFixed[i]) + ' ' + trackNameFixed[i] + '.m4a')
        print("Done!")
    except KeyboardInterrupt:
        break
    except:
        print("Failed to download " + trackName[i] + " (Track " + str(i + 1) + " of " + str(len(trackName)) + ").")
        continue
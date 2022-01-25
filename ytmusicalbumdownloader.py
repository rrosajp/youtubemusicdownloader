from logging import exception
from ytmusicapi import YTMusic
import yt_dlp
from mutagen.mp4 import MP4, MP4Cover
import urllib.request
import os

# ask user input
ytmusic = YTMusic()
playlistLinkInput = input('Enter a YouTube Music album link: ')[-41:]
albumBrowseId = ytmusic.get_album_browse_id(playlistLinkInput)

# check if its a valid link
while albumBrowseId is None:
    playlistLinkInput = input('Invalid input. Enter a YouTube Music album link: ')[-41:]
    albumBrowseId = ytmusic.get_album_browse_id(playlistLinkInput)

# save raw album info
albumRawInfo = ytmusic.get_album(albumBrowseId)

albumTrackArtist = []
albumTrackName = []
albumName = []
albumArtist = []
albumTrackPosition = []
albumCoverUrl = []

albumTrackNameFixed = []
albumNameFixed = []
albumArtistFixed = []


for i in range(albumRawInfo['trackCount']):

    # save track artist
    if albumRawInfo['tracks'][i]['artists'] == None:
        albumTrackArtist.append(albumRawInfo['artists'][0]['name'])
    else:
        albumTrackArtist.append(albumRawInfo['tracks'][i]['artists'][0]['name'])

    # save album track list
    albumTrackName.append(albumRawInfo['tracks'][i]['title'])

    albumTrackNameFixed.append(albumRawInfo['tracks'][i]['title'])

# save album name
albumName.append(albumRawInfo['title'])

albumNameFixed.append(albumRawInfo['title'])

# save album artist
albumArtist.append(albumRawInfo['artists'][0]['name'])

albumArtistFixed.append(albumRawInfo['artists'][0]['name'])

# save album track count & format it
for i in range(albumRawInfo['trackCount']):
    albumTrackPosition.append("%02d" % (i + 1))

# save album cover url
albumCoverUrl = albumRawInfo['thumbnails'][0]['url'].replace('w60-h60', 'w1200-h1200')

# remove illegal characters from album track list
for i in range(len(albumTrackName)):
    albumTrackNameFixed[i] = albumTrackNameFixed[i].replace('\\', '_')
    albumTrackNameFixed[i] = albumTrackNameFixed[i].replace('/', '_')
    albumTrackNameFixed[i] = albumTrackNameFixed[i].replace(':', '_')
    albumTrackNameFixed[i] = albumTrackNameFixed[i].replace('*', '_')
    albumTrackNameFixed[i] = albumTrackNameFixed[i].replace('?', '_')
    albumTrackNameFixed[i] = albumTrackNameFixed[i].replace('"', '_')
    albumTrackNameFixed[i] = albumTrackNameFixed[i].replace('<', '_')
    albumTrackNameFixed[i] = albumTrackNameFixed[i].replace('>', '_')
    albumTrackNameFixed[i] = albumTrackNameFixed[i].replace('|', '_')

# remove illegal characters from album artist
albumArtistFixed[0] = albumArtistFixed[0].replace('\\', '_')
albumArtistFixed[0] = albumArtistFixed[0].replace('/', '_')
albumArtistFixed[0] = albumArtistFixed[0].replace(':', '_')
albumArtistFixed[0] = albumArtistFixed[0].replace('*', '_')
albumArtistFixed[0] = albumArtistFixed[0].replace('?', '_')
albumArtistFixed[0] = albumArtistFixed[0].replace('"', '_')
albumArtistFixed[0] = albumArtistFixed[0].replace('<', '_')
albumArtistFixed[0] = albumArtistFixed[0].replace('>', '_')
albumArtistFixed[0] = albumArtistFixed[0].replace('|', '_')

# remove illegal characters from album name
albumNameFixed[0] = albumNameFixed[0].replace('\\', '_')
albumNameFixed[0] = albumNameFixed[0].replace('/', '_')
albumNameFixed[0] = albumNameFixed[0].replace(':', '_')
albumNameFixed[0] = albumNameFixed[0].replace('*', '_')
albumNameFixed[0] = albumNameFixed[0].replace('?', '_')
albumNameFixed[0] = albumNameFixed[0].replace('"', '_')
albumNameFixed[0] = albumNameFixed[0].replace('<', '_')
albumNameFixed[0] = albumNameFixed[0].replace('>', '_')
albumNameFixed[0] = albumNameFixed[0].replace('|', '_')
 
# show download step
print(albumName[0] + ' - ' + albumArtist[0])

# download cover
urllib.request.urlretrieve(albumCoverUrl, 'Cover.jpg')

# start downloading and get lyrics
for i in range(len(albumTrackPosition)):
    if os.path.exists('YouTube Music/' + albumArtistFixed[0] + '/' + albumNameFixed[0] + '/' + str(albumTrackPosition[i]) + ' ' + albumTrackNameFixed[i] + '.m4a') == True:
        pass
    else:
        print('Downloading ' + '\"' + albumTrackName[i] + '\"' + ' (Track ' + str(i + 1) + ' of ' + str(albumRawInfo['trackCount']) + ')')
        try:
            ydl_opts = {
            'format': '141/140',
            'cookiefile': 'cookies.txt',
            'outtmpl': 'YouTube Music/' + albumArtistFixed[0] + '/' + albumNameFixed[0] + '/' + str(albumTrackPosition[i]) + ' ' + albumTrackNameFixed[i] + '.m4a',
            'playliststart': i + 1,
            'playlistend': i + 1,
            'quiet': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download('https://music.youtube.com/playlist?list=' + playlistLinkInput)
                downloadInfo = ydl.extract_info('https://music.youtube.com/playlist?list=' + playlistLinkInput, download=False)
            albumTrackLyricsId = ytmusic.get_watch_playlist(downloadInfo['entries'][0]['display_id'])
            albumTrackLyrics = ytmusic.get_lyrics(albumTrackLyricsId['lyrics'])
            print('Done!')
            tags = MP4('YouTube Music/' + albumArtistFixed[0] + '/' + albumNameFixed[0] + '/' + str(albumTrackPosition[i]) + ' ' + albumTrackNameFixed[i] + '.m4a').tags
            tags['\xa9nam'] = albumTrackName[i]
            tags['\xa9alb'] = albumName[0]
            tags['aART'] = albumArtist[0]
            tags['\xa9day'] = albumRawInfo['year']
            tags['\xa9ART'] = albumTrackArtist[i]
            tags['trkn'] = [(i + 1, albumRawInfo['trackCount'])]
            with open('Cover.jpg', "rb") as cover:
                tags["covr"] = [
                MP4Cover(cover.read(), imageformat=MP4Cover.FORMAT_JPEG)
            ]
            if albumTrackLyrics['lyrics'] is None:
                i += 0
            else:
                tags['\xa9lyr'] = albumTrackLyrics['lyrics']
            tags.save('YouTube Music/' + albumArtistFixed[0] + '/' + albumNameFixed[0] + '/' + str(albumTrackPosition[i]) + ' ' + albumTrackNameFixed[i] + '.m4a')
        except:
            pass
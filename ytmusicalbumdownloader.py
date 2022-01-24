from ytmusicapi import YTMusic
import yt_dlp

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
albumTrackList = []
albumName = []
albumArtist = []

albumTrackListFixed = []
albumNameFixed = []
albumArtistFixed = []
albumTrackCount = []

for i in range(albumRawInfo['trackCount']):

    # save track artist
    if albumRawInfo['tracks'][i]['artists'] == None:
        albumTrackArtist.append(albumRawInfo['artists'][0]['name'])
        albumTrackArtist.append(albumRawInfo['artists'][0]['name'])
    else:
        albumTrackArtist.append(albumRawInfo['tracks'][i]['artists'][0]['name'])

    # save album track list
    albumTrackList.append(albumRawInfo['tracks'][i]['title'])

    albumTrackListFixed.append(albumRawInfo['tracks'][i]['title'])

# save album name
albumName.append(albumRawInfo['title'])

albumNameFixed.append(albumRawInfo['title'])

# save album artist
albumArtist.append(albumRawInfo['artists'][0]['name'])

albumArtistFixed.append(albumRawInfo['artists'][0]['name'])

# save album track count and format it
for i in range(albumRawInfo['trackCount']):
    if albumRawInfo['trackCount'] > 100:
        albumTrackCount.append("%03d" % (i + 1))
    else:
        albumTrackCount.append("%02d" % (i + 1))

# remove illegal characters from album track list
for i in range(len(albumTrackList)):
    albumTrackListFixed[i] = albumTrackListFixed[i].replace('\\', '_')
    albumTrackListFixed[i] = albumTrackListFixed[i].replace('/', '_')
    albumTrackListFixed[i] = albumTrackListFixed[i].replace(':', '_')
    albumTrackListFixed[i] = albumTrackListFixed[i].replace('*', '_')
    albumTrackListFixed[i] = albumTrackListFixed[i].replace('?', '_')
    albumTrackListFixed[i] = albumTrackListFixed[i].replace('"', '_')
    albumTrackListFixed[i] = albumTrackListFixed[i].replace('<', '_')
    albumTrackListFixed[i] = albumTrackListFixed[i].replace('>', '_')
    albumTrackListFixed[i] = albumTrackListFixed[i].replace('|', '_')

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
print('Downloading ' + albumName[0] + ' by ' + albumArtist[0] + '...')

# start downloading
for i in range(albumRawInfo['trackCount']):
    ydl_opts = {
    'format': '141/140',
    'cookiefile': 'cookies.txt',
    'outtmpl': str(albumTrackCount[i]) + ' ' + albumTrackListFixed[i] + '.m4a'
}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download('https://music.youtube.com/watch?v=' + albumRawInfo['tracks'][i]['videoId'])

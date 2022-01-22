from queue import Empty
from types import NoneType
from ytmusicapi import YTMusic
import json
import yt_dlp

ytmusic = YTMusic('headers_auth.json')
playlistidinput = input('Insert a YouTube Music album playlist ID: ')
albumid = ytmusic.get_album_browse_id(playlistidinput)
while albumid is None:
    playlistidinput = input('Invalid playlist ID. Insert a YouTube Music album playlist ID: ')
    albumid = ytmusic.get_album_browse_id(playlistidinput)
albuminfo = ytmusic.get_album(albumid)
albumname = albuminfo['title']
albumartistname = albuminfo['artists'][0]['name']
albumyear = albuminfo['year']
albumtotaltracks = albuminfo['trackCount']
albumduration = albuminfo['duration']
albumtrackinfo = albuminfo['tracks']
print("\nAlbum info:")
print("\nName: " + albumname)
print("Artist: " + albumartistname)
print("Year: " + albumyear)
print("Total track(s): " + str(albumtotaltracks))
print("Duration: " + albumduration + "\n")
arrayTratado = []
print("Album tracklist:\n")
for i in range(albumtotaltracks):
    albumtrackartist = 'churrasqueira controle remoto'
    if albumtrackinfo[0]['artists'] == None:
        albumtrackartist = albumartistname
    else:
        albumtrackartist = albumtrackinfo[i]['artists'][0]['name']
    dataSetTrack = { 'title': albumtrackinfo[i]['title'],  'artists': albumtrackartist
        ,'explicit': albumtrackinfo[i]['isExplicit']}
    json_dump = json.dumps(dataSetTrack)
    json_object = json.loads(json_dump)
    arrayTratado.append(json_object)
    print(str(i + 1) + " - " + json_object['artists'] + " - " + json_object['title'])
print('\nDownloading album...')
ydl_opts = {
    'format': '141/140',
    'cookiefile': 'cookies.txt',
    'outtmpl': '%(playlist_index)s.m4a'
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://music.youtube.com/playlist?list=' + playlistidinput])

from queue import Empty
from types import NoneType
from ytmusicapi import YTMusic
import json
import yt_dlp
from mutagen.mp4 import MP4

ytmusic = YTMusic('headers_auth.json')
playlistidinput = input('Insert a YouTube Music album playlist ID: ')
albumid = ytmusic.get_album_browse_id(playlistidinput)
while albumid is None:
    playlistidinput = input('Invalid playlist ID. Insert a YouTube Music album playlist ID: ')
    albumid = ytmusic.get_album_browse_id(playlistidinput)
albuminfo = ytmusic.get_album(albumid)
albumname = albuminfo['title']
albumartist = albuminfo['artists'][0]['name']
albumyear = albuminfo['year']
albumtotaltracks = albuminfo['trackCount']
albumduration = albuminfo['duration']
albumtrackinfo = albuminfo['tracks']
albumcover = albuminfo['thumbnails'][0]['url'][:-15] + '=w1024-h1024-l90-rj'
print("\nAlbum info:")
print("\nName: " + albumname)
print("Artist: " + albumartist)
print("Year: " + albumyear)
print("Total track(s): " + str(albumtotaltracks))
print("Duration: " + albumduration)
print("Cover: " + albumcover + "\n")
arrayTratado = []
print("Album tracklist (Track number/Artist/Title/Explicit):\n")
for i in range(albumtotaltracks):
    albumtrackartist = ''
    if albumtrackinfo[0]['artists'] == None:
        albumtrackartist = albumartist
    else:
        albumtrackartist = albumtrackinfo[i]['artists'][0]['name']
    dataSetTrack = { 'title': albumtrackinfo[i]['title'],  'artists': albumtrackartist
        ,'explicit': albumtrackinfo[i]['isExplicit']}
    json_dump = json.dumps(dataSetTrack)
    json_object = json.loads(json_dump)
    arrayTratado.append(json_object)
    print(str(i + 1) + " - " + json_object['artists'] + " - " + json_object['title'] + " - " + str(json_object['explicit']))
print('\nDownloading album...\n')
ydl_opts = {
    'format': '141/140',
    'cookiefile': 'cookies.txt',
    'outtmpl': '%(playlist_index)s.m4a'
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://music.youtube.com/playlist?list=' + playlistidinput])
print('\nAdding tags...\n')
for a in range(albumtotaltracks):
    tags = MP4(str(a + 1) + '.m4a').tags
    tags['\xa9nam'] = arrayTratado[a]['title']
    tags['\xa9alb'] = albumname
    tags['aART'] = albumartist
    tags['\xa9day'] = albumyear
    tags['\xa9ART'] = arrayTratado[a]['artists']
    tags['trkn'] = str(albumtotaltracks)
    tags.save(str(a + 1) + '.m4a')
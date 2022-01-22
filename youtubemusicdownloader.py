from queue import Empty
from types import NoneType
from ytmusicapi import YTMusic
import json
import yt_dlp
from mutagen.mp4 import MP4, MP4Cover
import urllib.request
import os

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
albumcover = albuminfo['thumbnails'][3]['url']
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
    dataSetTrack = { 'title': albumtrackinfo[i]['title'],  'artists': albumtrackartist}
    json_dump = json.dumps(dataSetTrack)
    json_object = json.loads(json_dump)
    arrayTratado.append(json_object)
    print(str(i + 1) + " - " + json_object['artists'] + " - " + json_object['title'])
print('\nDownloading album...\n')
ydl_opts = {
    'format': '141/140',
    'cookiefile': 'cookies.txt',
    for b range(albumtotaltracks):
        'outtmpl': '%(playlist_index)02d' + " " + arrayTratado[b]['title'] + '.m4a'
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://music.youtube.com/playlist?list=' + playlistidinput])
print('\nAdding tags & renaming files...\n')
urllib.request.urlretrieve(albumcover, 'Cover.jpg')
for a in range(albumtotaltracks):
    tags = MP4(str("%02d" % (a + 1,)) + '.m4a').tags
    tags['\xa9nam'] = arrayTratado[a]['title']
    tags['\xa9alb'] = albumname
    tags['aART'] = albumartist
    tags['\xa9day'] = albumyear
    tags['\xa9ART'] = arrayTratado[a]['artists']
    with open('Cover.jpg', "rb") as cover:
        tags["covr"] = [
        MP4Cover(cover.read(), imageformat=MP4Cover.FORMAT_JPEG)
        ]
    tags.save(str("%02d" % (a + 1,)) + '.m4a')
    os.rename(str("%02d" % (a + 1,)) + '.m4a', str("%02d" % (a + 1,)) + " " + arrayTratado[a]['title'] +'.m4a')
print('\nDone!\n')
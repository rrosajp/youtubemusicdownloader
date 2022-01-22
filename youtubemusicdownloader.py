from queue import Empty
from types import NoneType
from ytmusicapi import YTMusic

ytmusic = YTMusic('headers_auth.json')
playlistidinput = input('Insert a YouTube Music album playlist ID: ')
albumid = ytmusic.get_album_browse_id(playlistidinput)
while albumid is None:
    playlistidinput = input('Invalid playlist ID. Insert a YouTube Music album playlist ID: ')
    albumid = ytmusic.get_album_browse_id(playlistidinput)
albuminfo = ytmusic.get_album(albumid)
print("Album name: " + albuminfo['title'])
print("Album artist name: " + albuminfo['artists'][0]['name'])
print("Album year: " + albuminfo['year'])
print("Album total track(s): " + str(albuminfo['trackCount']))
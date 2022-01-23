from ytmusicapi import YTMusic

# ask user input
ytmusic = YTMusic()
playlistLinkInput = input('Enter a YouTube Music album link: ')[-41:]
browseId = ytmusic.get_album_browse_id(playlistLinkInput)

# check if its a valid link
while browseId is None:
    playlistLinkInput = input('Invalid input. Enter a YouTube Music album link: ')[-41:]
    browseId = ytmusic.get_album_browse_id(playlistLinkInput)

# start downloading
print("hello")
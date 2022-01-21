from ytmusicapi import YTMusic
import yt_dlp

ytmusic = YTMusic('headers_auth.json')
search = input("insira um link ou pesquise por algo: ")
result = ytmusic.search(search, filter = 'albums')
print("\n1:")
print("nome do album: " + result[0]["title"])
print("nome do artista: " + result[0]["artists"][0]["name"])
browseid1 = result[0]["browseId"]
print("\n2:")
print("nome do album: " + result[1]["title"])
print("nome do artista: " + result[1]["artists"][0]["name"])
browseid2 = result[1]["browseId"]
print("\n3:")
print("nome do album: " + result[2]["title"])
print("nome do artista: " + result[2]["artists"][0]["name"])
browseid3 = result[2]["browseId"]
choice = int(input("\ninsira qual opção tu quer: "))
while choice > 3 or choice < 0:
    choice = int(input("opção inexistente. insira qual dos álbuns tu quer: "))
if choice == 1:
    browseid = browseid1
if choice == 2:
    browseid = browseid2
    print("maneiro")
if choice == 3:
    browseid = browseid3
print("ganhaste")

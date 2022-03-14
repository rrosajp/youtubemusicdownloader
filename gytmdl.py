from ytmusicapi import YTMusic
import argparse
import yt_dlp
import requests
import platform
import os
import music_tag
from mutagen.mp4 import MP4, MP4Cover

ytmusic = YTMusic()

parser = argparse.ArgumentParser(description='Download YouTube Music tracks.')
parser.add_argument(
    'url',
    help='Any valid YouTube Music URL.',
    nargs='+',
)
parser.add_argument(
    "--f",
    "--format",
    default='140',
    help='141 (AAC 256kbps), 251 (Opus 160kbps) or 140 (AAC 128kbps). Requires a valid cookie file for 141. '
         'Default is 140.',
)
parser.add_argument(
    '--e',
    '--excludetags',
    default='',
    help='Any valid tag ("album", "albumartist", "artist", "artwork", "lyrics", "rating", "totaltracks", "tracknumber",'
         ' "tracktitle" and "year") separated by comma with no spaces.',
)
parser.add_argument(
    '--d',
    '--downloadartwork',
    action='store_true',
    help='Download artwork as "Cover.jpg" in download directory.',
)
parser.add_argument(
    '--a',
    '--artworksize',
    default='1200',
    help='"max" or any valid number. Default is "1200".'
)
args = parser.parse_args()
url = args.url
download_format = args.f
exclude_tags_options = args.e
artwork = args.d
size = args.a

def get_video_id(url):
    ydl_opts = {
        'extract_flat': True,
        'skip_download': True,
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        url_details = ydl.extract_info(
            url,
            download=False,
        )

    if 'youtube' in url_details['extractor']:
        if 'MPREb' in url_details['webpage_url_basename']:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                url_details = ydl.extract_info(
                    url_details['url'],
                    download=False,
                )

        if 'playlist' in url_details['webpage_url_basename']:
            video_id = []
            for a in range(len(url_details['entries'])):
                video_id_details = ytmusic.get_song(url_details['entries'][a]['id'])
                if 'streamingData' in video_id_details:
                    video_id.append(url_details['entries'][a]['id'])
            if video_id:
                return video_id

        if 'watch' in url_details['webpage_url_basename']:
            video_id_details = ytmusic.get_song(url_details['id'])
            if 'streamingData' in video_id_details:
                return [url_details['id']]


def check_artwork_size(artwork_size):
    if artwork_size == 'max':
        return '16383'
    else:
        try:
            if (int(artwork_size) > 0) or (int(artwork_size) < 16384):
                return artwork_size
            else:
                return '1200'
        except:
            return '1200'


def get_tags(video_id, artwork_size):
    illegal_characters = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    watch_playlist = ytmusic.get_watch_playlist(video_id)
    album_details = ytmusic.get_album(watch_playlist['tracks'][0]['album']['id'])
    album = album_details['title']
    album_fixed = album
    if len(album_details['artists']) == 1:
        album_artist = album_details['artists'][0]['name']
    else:
        album_artist = album_details['artists'][0]['name'] + ' & ' + album_details['artists'][1]['name']
    album_artist_fixed = album_artist
    if len(watch_playlist['tracks'][0]['artists']) == 1:
        artist = watch_playlist['tracks'][0]['artists'][0]['name']
    else:
        artist = watch_playlist['tracks'][0]['artists'][0]['name'] + ' & ' + \
                 watch_playlist['tracks'][0]['artists'][1]['name']
    artist_fixed = artist
    artwork = requests.get(album_details['thumbnails'][0]['url'].split('=')[0] + '=w' + artwork_size).content
    try:
        lyrics_id = ytmusic.get_lyrics(watch_playlist['lyrics'])
        lyrics = lyrics_id['lyrics']
    except:
        lyrics = None
    rating = 0
    track_number = 0
    track_number_fixed = 00
    total_tracks = album_details['trackCount']
    ydl_opts = {
        'extract_flat': True,
        'skip_download': True,
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        album_playlist_details = ydl.extract_info(
            'https://music.youtube.com/playlist?list='
            + album_details['audioPlaylistId'],
            download=False,
        )
    for a in range(len(album_playlist_details['entries'])):
        if album_playlist_details['entries'][a]['id'] == video_id:
            if album_details['tracks'][a]['isExplicit']:
                rating = 4
            else:
                rating = 0
            track_number = 1 + a
            track_number_fixed = '%02d' % (1 + a)
    track_title = watch_playlist['tracks'][0]['title']
    track_title_fixed = track_title
    year = album_details['year']
    for a in range(len(illegal_characters)):
        album_artist_fixed = album_artist_fixed.replace(illegal_characters[a], '_')
        album_fixed = album_fixed.replace(illegal_characters[a], '_')
        artist_fixed = artist_fixed.replace(illegal_characters[a], '_')
        track_title_fixed = track_title_fixed.replace(illegal_characters[a], '_')
    if album_artist_fixed.endswith('.'):
        album_artist_fixed = album_artist_fixed.replace('.', '_')
    if album_fixed.endswith('.'):
        album_fixed = album_fixed.replace('.', '_')
    return {
        'album': album,
        'album_fixed': album_fixed,
        'album_artist': album_artist,
        'album_artist_fixed': album_artist_fixed,
        'artist': artist,
        'artist_fixed': artist_fixed,
        'artwork': artwork,
        'lyrics': lyrics,
        'rating': rating,
        'total_tracks': total_tracks,
        'track_number': track_number,
        'track_number_fixed': track_number_fixed,
        'track_title': track_title,
        'track_title_fixed': track_title_fixed,
        'video_id': video_id,
        'year': year,
    }


def get_download_options(download_format, tags):
    extension = ''
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    if download_format == '141' or download_format == '140':
        extension = '.m4a'
    if download_format == '141':
        ydl_opts['cookiefile'] = 'cookies.txt'
        ydl_opts['format'] = '141'
    elif download_format == '251':
        extension = '.opus'
        ydl_opts['format'] = '251'
        ydl_opts['postprocessors'] = [
            {
                'key': 'FFmpegExtractAudio',
            }
        ]
    elif download_format == '140':
        ydl_opts['format'] = '140'
    else:
        extension = '.m4a'
        ydl_opts['format'] = '140'
    if platform.system() == 'Windows':
        current_directory = '\\\\?\\' + os.getcwd()
        slash = '\\'
    else:
        current_directory = os.getcwd()
        slash = '/'
    ydl_opts['outtmpl'] = current_directory + slash + 'YouTube Music' + slash + tags['album_artist_fixed'] + slash \
                         + tags['album_fixed'] + slash + tags['track_number_fixed'] + ' ' + tags['track_title_fixed'] \
                         + extension
    artwork_download_directory = current_directory + slash + 'YouTube Music' + slash + tags['album_artist_fixed']\
                                 + slash + tags['album_fixed'] + slash
    return [ydl_opts, artwork_download_directory]


def download(download_options, tags):
    with yt_dlp.YoutubeDL(download_options[0]) as ydl:
        ydl.download('https://music.youtube.com/watch?v=' + tags['video_id'])


def get_exclude_tags(exclude_tags_options):
    exclude_tags = {
        'album': False,
        'albumartist': False,
        'artist': False,
        'artwork': False,
        'lyrics': False,
        'rating': False,
        'totaltracks': False,
        'tracknumber': False,
        'tracktitle': False,
        'year': False,
        'all': False,
    }
    if exclude_tags_options != '':
        exclude_tags_options = exclude_tags_options.split(',')
        for a in range(len(exclude_tags_options)):
            exclude_tags[exclude_tags_options[a]] = True
    return exclude_tags


def apply_tags(download_options, exclude_tags, tags):
    if not exclude_tags['all']:
        if download_options[0]['format'] == '251':
            file = music_tag.load_file(download_options[0]['outtmpl'])
            if not exclude_tags['album']:
                file['album'] = tags['album']
            if not exclude_tags['albumartist']:
                file['albumartist'] = tags['album_artist']
            if not exclude_tags['artist']:
                file['artist'] = tags['artist']
            if not exclude_tags['artwork']:
                file['artwork'] = tags['artwork']
            if not exclude_tags['lyrics']:
                if tags['lyrics'] is not None:
                    file['lyrics'] = tags['lyrics']
            if not exclude_tags['totaltracks']:
                file['totaltracks'] = tags['total_tracks']
            if not exclude_tags['tracknumber']:
                file['tracknumber'] = tags['track_number']
            if not exclude_tags['tracktitle']:
                file['tracktitle'] = tags['track_title']
            if not exclude_tags['year']:
                file['year'] = tags['year']
            file.save()
        else:
            file = MP4(download_options[0]['outtmpl']).tags
            if not exclude_tags['album']:
                file['\xa9alb'] = tags['album']
            if not exclude_tags['albumartist']:
                file['aART'] = tags['album_artist']
            if not exclude_tags['artist']:
                file['\xa9ART'] = tags['artist']
            if not exclude_tags['artwork']:
                file['covr'] = [MP4Cover(tags['artwork'], imageformat=MP4Cover.FORMAT_JPEG)]
            if not exclude_tags['lyrics']:
                if tags['lyrics'] is not None:
                    file['\xa9lyr'] = tags['lyrics']
            if not exclude_tags['tracktitle']:
                file['\xa9nam'] = tags['track_title']
            if not exclude_tags['totaltracks']:
                file['trkn'] = [(0, tags['total_tracks'])]
                if not exclude_tags['tracknumber']:
                    file['trkn'] = [(tags['track_number'], tags['total_tracks'])]
            if not exclude_tags['tracknumber']:
                file['trkn'] = [(tags['track_number'], 0)]
                if not exclude_tags['totaltracks']:
                    file['trkn'] = [(tags['track_number'], tags['total_tracks'])]
            if not exclude_tags['rating']:
                file['rtng'] = [tags['rating']]
            if not exclude_tags['year']:
                file['\xa9day'] = tags['year']
            file.save(download_options[0]['outtmpl'])


def download_artwork(artwork, download_options, tags):
    if artwork:
        with open(
            download_options[1] + 'Cover.jpg', 'wb'
        ) as cover_file:
            cover_file.write(tags['artwork'])


def main(url, size, download_format, artwork, exclude_tags_options):
    error_count = 0
    print('Checking URL...')
    video_id = []
    for a in range(len(url)):
        try:
            video_id += get_video_id(url[a])
        except:
            pass
    if not video_id:
        exit('No valid URL entered.')
    for a in range(len(video_id)):
        print(f'Getting tags (Track {str(a + 1)} of {str(len(video_id))})...')
        try:
            artwork_size = check_artwork_size(size)
            tags = get_tags(video_id[a], artwork_size)
            print(f'Downloading "{tags["track_title"]}" (Track {str(a + 1)} of {str(len(video_id))})...')
            download_options = get_download_options(download_format, tags)
            download(download_options, tags)
            exclude_tags = get_exclude_tags(exclude_tags_options)
            apply_tags(download_options, exclude_tags, tags)
            download_artwork(artwork, download_options, tags)
            print(f'Download finished "{tags["track_title"]}" (Track {str(a + 1)} of {str(len(video_id))})!')
        except KeyboardInterrupt:
            exit()
        except:
            print(f'* Download failed (Track {str(a + 1)} of {str(len(video_id))}).')
            error_count += 1
            pass
    exit(f'All done. ({error_count} errors.)')


main(url, size, download_format, artwork, exclude_tags_options)

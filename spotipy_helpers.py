import datetime
import csv
import spotipy
import spotipy.util as util
import json

SPOTIPY_CLIENT_ID='4b8925015d0b47d9b9bf719ebe5cf882'
SPOTIPY_CLIENT_SECRET='833d5ca3bdab45a0b7713c13aa1733ee'
SPOTIPY_REDIRECT_URI='http://localhost/'

def authenticate_spotipy(username):
  scope = 'playlist-modify-public'
  token = util.prompt_for_user_token(username, scope,client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI)
  if token:
    return spotipy.Spotify(auth=token)
  else:
    print('Authentication to Spotify Failed')
    raise

def find_or_create_playlist(sp, username, user_playlists, playlist_name):
  playlist_name = playlist_name or f'Spotify Import {datetime.datetime.now().strftime("%b %d %Y")}'
  playlistfound = list(filter(lambda d: d['name'] in [f'{playlist_name}'], user_playlists))
  if not playlistfound:
    return sp.user_playlist_create(username, playlist_name)['id']
  else:
    return playlistfound[0]['id']

def add_songs_from_csv(sp, csv_file, username, playlist_id, songs_not_found):
  with open(csv_file, newline='') as csv_file:
    song_reader = csv.reader(csv_file)
    counter = 0
    song_ids = []
    for row in song_reader:
      response = find_song(sp, row[0], row[1])  
      if response:
        counter += 1
        first_song = response[0]
        song_ids.append(first_song['id'])
        print("Found {0} by {1}".format(first_song['name'], first_song['album']['artists'][0]['name']))
        if counter % 100 == 0:
          sp.user_playlist_add_tracks(username, playlist_id, song_ids)
          song_ids = []
          counter = 0
      else:
        songs_not_found.write(f"{row[0]},{row[1]}\r\n")
    sp.user_playlist_add_tracks(username, playlist_id, song_ids)

def add_songs_from_csv_genre(sp, csv_file, username, playlists_by_genre, playlist_hash, songs_not_found):
  with open(csv_file, newline='') as csv_file:
    song_reader = csv.reader(csv_file)
    for row in song_reader:
      response = find_song(sp, row[0], row[1])  
      if response:
        playlist_key = playlists_by_genre[row[2]] if row[2] in playlists_by_genre else 'OG Misc'
        first_song = response[0]
        playlist_hash[playlist_key]['song_ids'].append(first_song['id'])
        print("Found {0} by {1} for playlist {2}".format(first_song['name'], first_song['album']['artists'][0]['name'], playlist_key))
        if len(playlist_hash[playlist_key]['song_ids']) % 100 == 0:
          sp.user_playlist_add_tracks(username, playlist_hash[playlist_key]['playlist_id'], playlist_hash[playlist_key]['song_ids'])
          playlist_hash[playlist_key]['song_ids'] = []
      else:
        songs_not_found.write(f"{row[0]},{row[1]}\r\n")
    for playlist in playlist_hash:
      if len(playlist_hash[playlist]['song_ids']) > 0:
        sp.user_playlist_add_tracks(username, playlist_hash[playlist]['playlist_id'], playlist_hash[playlist]['song_ids'])


def find_song(sp, songname, artist):
  query = f'artist:%{artist} track:%{songname}'
  return sp.search(q=query, type='track')['tracks']['items']

def parse_playlists_from_genre(sp, username, user_playlists, playlists_by_genre):
    playlists = set(val for val in playlists_by_genre.values())
    playlist_hash = { playlist: { "playlist_id": None, "song_ids": [] } for playlist in playlists }
    for playlist in playlist_hash.keys():
      playlist_hash[playlist]['playlist_id'] = find_or_create_playlist(sp, username, user_playlists, playlist)
    return playlist_hash
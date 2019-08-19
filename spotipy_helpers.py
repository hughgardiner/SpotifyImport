import datetime
import csv
import spotipy
import spotipy.util as util
import json

def authenticate_spotipy(username):
  scope = 'playlist-modify-public'
  token = util.prompt_for_user_token(username, scope)
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

def add_songs_from_csv(sp, csv_file, username, playlist_id, songs_not_found, batch_size):
  batch_size = batch_size or 100
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
        if counter % batch_size == 0:
          sp.user_playlist_add_tracks(username, playlist_id, song_ids)
          song_ids = []
          counter = 0
      else:
        songs_not_found.write(f"{row[0]},{row[1]}\r\n")
    sp.user_playlist_add_tracks(username, playlist_id, song_ids)

def find_song(sp, songname, artist):
  query = f'artist:%{artist} track:%{songname}'
  return sp.search(q=query, type='track')['tracks']['items']
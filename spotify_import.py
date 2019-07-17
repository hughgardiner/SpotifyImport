import sys
import spotipy
import spotipy.util as util
import csv

username = sys.argv[1]
playlist_name = sys.argv[2]
csv_file_name = sys.argv[3]

scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope)

if token:
  sp = spotipy.Spotify(auth=token)
  user_playlists = sp.user_playlists(username)['items']

  if user_playlists:
    playlist_id = find_or_create_playlist(sp, playlist_name, user_playlists)
    
    songs_not_found = open("songs_not_found.txt","w+")
    with open(csv_file_name, newline='') as csv_file:
      song_reader = csv.reader(csv_file)
      for row in song_reader:
        response = find_song(sp, row[0], row[1])
        if response:
          print(response[0]['id'])
          sp.user_playlist_add_tracks(username, playlist_id, [response[0]['id']])
        else:
           songs_not_found.write("Couldn't find song %s by %s\r\n" % row[0], row[1])

else:
  print('Authentication to Spotify Failed')

def find_song(sp, songname, artist):
  query = f'artist:%{artist} track:%{songname}'
  print(f'Query = {query}')
  return sp.search(q=query, type='track')['tracks']['items']

def find_or_create_playlist(sp, playlist_name, user_playlists):
  playlistfound = list(filter(lambda d: d['name'] in [f'{playlist_name}'], user_playlists))
  if not playlistfound:
    return sp.user_playlist_create(username, playlist_name)['id']
  else:
    return playlistfound[0]['id']
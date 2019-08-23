import sys
import spotipy
import spotipy.util as util
import argparse
import yaml
from spotipy_helpers import *

parser = argparse.ArgumentParser(description='Import songs to Spotify from Textfile')
parser.add_argument('username', type=str, help='Spotify Username')
parser.add_argument('filename', type=str, help='Name of Textfile for import')
parser.add_argument('-p', '--playlist', type=str, help='Name of playlist to import songs into')
parser.add_argument('-g', '--genre', type=str, help='Include yaml file categorizing subgenres into playlists')
args = parser.parse_args()

def validate_inputs(args):
  if args.genre is not None and args.playlist is not None:
    print('Both playlist and genre flags cannot be specified')
    sys.exit(1)

validate_inputs(args)

sp = authenticate_spotipy(args.username)
user_playlists = sp.user_playlists(args.username)['items']

timestamp = datetime.datetime.now().strftime("%m_%d_%Y_%X")
songs_not_found = open(f'songs_not_found_{timestamp}.csv',"w")
if args.genre is not None:
  playlist_hash = {}
  with open(args.genre, 'r') as genre_file:
    playlists_by_genre = yaml.safe_load(genre_file)
    if type(playlists_by_genre) is not dict:
      print('Genre yaml file is not a valid format')
      sys.exit(1)
    playlist_hash = parse_playlists_from_genre(sp, args.username, user_playlists, playlists_by_genre)
  if playlist_hash:
    add_songs_from_csv_genre(sp, args.filename, args.username, playlists_by_genre, playlist_hash, songs_not_found)

else:
  playlist_id = find_or_create_playlist(sp, args.username, user_playlists, args.playlist)
  add_songs_from_csv(sp, args.filename, args.username, playlist_id, songs_not_found)

songs_not_found.close()

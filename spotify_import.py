import sys
import spotipy
import spotipy.util as util
import argparse
from spotipy_helpers import *

parser = argparse.ArgumentParser(description='Import songs to Spotify from Textfile')
parser.add_argument('username', type=str, help='Spotify Username')
parser.add_argument('filename', type=str, help='Name of Textfile for import')
parser.add_argument('-p', '--playlist', type=str, help='Name of playlist to import songs into')
parser.add_argument('-g', '--genre', action='store_true', help='Include yaml file categorizing subgenres into playlists')
parser.add_argument('-b', '--batch-size', type=int, help='Number of songs per Spotify API Request')
args = parser.parse_args()

sp = authenticate_spotipy(args.username)
user_playlists = sp.user_playlists(args.username)['items']

timestamp = datetime.datetime.now().strftime("%m_%d_%Y_%X")
songs_not_found = open(f'songs_not_found_{timestamp}.csv',"w")
if args.genre:
  print('Not yet implemented')
  exit
else:
  playlist_id = find_or_create_playlist(sp, args.username, user_playlists, args.playlist)
  add_songs_from_csv(sp, args.filename, args.username, playlist_id, songs_not_found, args.batch_size)

songs_not_found.close()

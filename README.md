# SpotifyImport

Command line utility to convert your Music Collections into Spotify Playlists.

## Getting Started
- Open a `Terminal`, clone repo locally then cd into `SpotifyImport`
```bash
git clone git@github.com:hughgardiner/SpotifyImport.git && cd SpotifyImport
```
- Install [Spotipy](https://spotipy.readthedocs.io/en/latest/)
```bash
pip install spotipy
```
- Convert your Music Libary into a CSV with columns `Song Name`, `Artist`, and `Genre` (optional unless utilizing [Import by Genre into Playlists](#import-by-genre-into-playlists))
```csv
Levels,Avicii,House
Gimme Shelter,The Rolling Stones,Rock
```
## Import into Single Playlist
- To import all songs into a single playlist, run the following command in your `Terminal`
```bash
python spotify_import.py SPOTIFY_USERNAME test_file.csv -p "Test Playlist"
```
- Log into the Spotify Redirect and copy the redirect URL from the browser navigation bar back into your terminal prompt (i.e. `http://localhost/?code=YOUR_SPOTIFY_ACCESS_TOKEN`)

## Import by Genre into Playlists
- If you'd like to utilize the import by Genre Feature, organize all Genres from your CSV into a yaml file with the following format:
```yaml
Playlist Name 1:
  - Rock
  - Alternative
  - Punk Rock
  - Acoustic
  - Classic Rock
Playlist Name 2:
  - Club
  - Trap
  - Electronic
  - Dance
  - House
  - Trance
  - Techno
```
- Once you have the genre yaml file, run the following command in your `Terminal`:
```bash
python spotify_import.py SPOTIFY_USERNAME test_file.csv -g example_genre_file.yml
```
- Your songs will then be organized in two seperate playlists based on the organization of genres in the Genre Yaml file.

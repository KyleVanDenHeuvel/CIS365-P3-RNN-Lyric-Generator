from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import lyricsgenius


#Stored as environmental variables
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#Should probably store this in separate file
genius_client_access = 'key'
genius = lyricsgenius.Genius(genius_client_access)

playlist_id = input("Please input a Spotify url:")

#track:artist format with which to search lyrics via Genius
search_tracks = []

#Gets the name of the input playlist
playlist_name = sp.playlist(playlist_id)['name']
#Removes any characters invalid for file naming
for char in playlist_name:
    if not char.isalnum():
        playlist_name = playlist_name.replace(char, "")

filename=playlist_name+".txt"

#Create a new file to write lyrics to
file = open(filename, "a", encoding="utf-8")

#Gets all playlist tracks instead of just 100
def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

results = get_playlist_tracks(playlist_id)

#Go through every track in the playlist & get the track title and artist name
for item in results:

    artist_names = [artist['name'] for artist in item['track']['artists']]
    track_title = item['track']['name']

    #Creating a single string we can split later
    track_and_artist = track_title+":"+artist_names[0]
    print(track_and_artist)

    search_tracks.append(track_and_artist)

skipped_count = 0
for track in search_tracks:

    #Splits the track and the artist
    track_and_artist = track.split(':')

    track = track_and_artist[0]
    artist = track_and_artist[1]

    #Searches for the given song and writes it to the file
    song = genius.search_song(track, artist)

    #Check to see that lyrics can be found for the given song
    if song is not None:
        file.write(song.lyrics)
    else:
        skipped_count+=1

print("Lyrics recorded for "+playlist_name+"!")
print("Skipped tracks: ", skipped_count)







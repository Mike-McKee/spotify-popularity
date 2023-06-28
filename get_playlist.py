import secret_id
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials as scc

#Gets my Spotify client id and client secret from different python file
client_id = secret_id.CLIENT_ID
client_secret = secret_id.CLIENT_SECRET

#Create Spotify client
cc_manager = scc(client_id = client_id, client_secret= client_secret)
spotify = spotipy.Spotify(client_credentials_manager=cc_manager)

#Get all tracks in my Canciones en Español playlist
playlist_name = '5nm9DmPdEB4PDJGlAofR6c'
requests = spotify.playlist_tracks(playlist_name)

data = [requests]

#turns playlist data into a json file
with open('playlist.json', 'w') as jsonfile:        #note: renamed playlist.json to first_test.json
    json.dump(data, jsonfile, indent=4)

#test to make sure program runs properly
print('================ ALL DONE. PLAYLIST DOWNLOADED ================')


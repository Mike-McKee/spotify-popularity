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
all_tracks = []
limit = 100
offset = 0

#Spotify API limmits requests to 100. Since the playlist has more songs than that,
#the while loop keeps requesting until we have every song
while True:
        requests = spotify.playlist_tracks(playlist_name, offset=offset, limit=limit)

        if 'items' in requests:
            all_tracks.extend(requests['items'])
            if len(requests['items']) < limit:
                break

            offset += limit

        else:
            print('Error Occurred')
            break

with open('playlist.json', 'w') as jsonfile:
    json.dump(all_tracks, jsonfile, indent=4)

#test to make sure program runs properly
print('================ ALL DONE. PLAYLIST DOWNLOADED ================')


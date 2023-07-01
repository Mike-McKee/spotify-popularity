#Code to get the artists data using Spotify's API
import secret_id
import time
import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials as scc

start = time.time()

client_id = secret_id.CLIENT_ID
client_secret = secret_id.CLIENT_SECRET

cc_manager = scc(client_id=client_id, client_secret=client_secret)
spotify = spotipy.Spotify(client_credentials_manager=cc_manager)

with open('artists.csv', 'r+') as file:
	artists = csv.reader(file)

	new_headers = ['Artist_Popularity', 'Top_Track_1', 'Top_Track_2', 'Top_Track_3',
				  'Top_Track_4', 'Top_Track_5', 'Top_Track_6', 'Top_Track_7', 
				  'Top_Track_8', 'Top_Track_9', 'Top_Track_10']
	
	header_row = next(artists)
	header_row.extend(new_headers)

	for row in artists:
		artist = spotify.artist(row[1])
		tracks = spotify.artist_top_tracks(row[1])

		artist_pop = artist['popularity']
		
		list_t = tracks['tracks']
		t_tracks = []
		for i in list_t:
			track = i['name']
			t_tracks.append(track)
		
		row.extend([artist_pop] + t_tracks)

	file.seek(0)
	writer = csv.writer(file)
	writer.writerow(header_row)
	writer.writerow(artists)


"""
So close...

We got the code to work and write in the csv, but it added all values to the end of the
csv as one GIANT list.

So we've gotta find a way to rewrite the file instead of just appending to it.
"""
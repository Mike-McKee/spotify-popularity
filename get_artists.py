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

with open('artists.csv', 'r') as file:
	artists = csv.reader(file)
	
	#skips the first row
	next(artists)

	artist_data = []
	for row in artists:
		artist = spotify.artist(row[1])
		tracks = spotify.artist_top_tracks(row[1])

		artist_pop = artist['popularity']
		
		list_t = tracks['tracks']
		t_tracks = []
		for i in list_t:
			track = i['name']
			t_tracks.append(track)

		new_row = row + [artist_pop] + [t for t in t_tracks] 
		artist_data.append(new_row)

with open('updated_artists.csv', 'w') as new_file:
	writer = csv.writer(new_file)
	
	header_row = ['Artist_Name', 'Artist_Id', 'Artist_Popularity', 'Top_Track_1', 'Top_Track_2', 'Top_Track_3',
				  'Top_Track_4', 'Top_Track_5', 'Top_Track_6', 'Top_Track_7', 
				  'Top_Track_8', 'Top_Track_9', 'Top_Track_10']
	
	writer.writerow(header_row)
	for k in artist_data:
		writer.writerow(k)

print("=====================SUCCESS=====================")

#Had some fun and tested how long this program takes to run.... Results below
end = time.time()
runtime = end - start
print(f"This program took {runtime} seconds to successfully run")

#First attempt took 73.03422427177429 seconds
#Second attempt took 81.47556614875793 seconds
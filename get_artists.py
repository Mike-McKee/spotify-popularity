#Code to get the artists data using Spotify's API


"""
what we need to do:
1. create list of artists names by iterating through playlist.csv and creating
list of all artists from 1-6 (be sure to not duplicate info... and save their 
names and id numbers)
2. create while loop to keep requesting data (and appending to an empty list) until
we have the info for every artist on the list)
3. While we're doing this, we might as well get the artists top tracks at the same
time using a separate request
"""
import secret_id
import json
import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials as scc

client_id = secret_id.CLIENT_ID
client_secret = secret_id.CLIENT_SECRET

cc_manager = scc(client_id=client_id, client_secret=client_secret)
spotify = spotipy.Spotify(client_credentials_manager=cc_manager)

def iterate_csv(file_name, column_name):
	with open(file_name, 'r') as file:
		playlist = csv.reader(file, delimiter=',')
		for row in playlist:
			value = row[column_name]
			return value

def get_artists(file_name):
	name_headers = ['Artist_1_Name', 'Artist_2_Name', 'Artist_3_Name', 
									'Artist_4_Name', 'Artist_5_Name', 'Artist_6_Name']
	id_headers = ['Artist_1_Popularity', 'Artist_2_Popularity', 'Artist_3_Popularity',
		            'Artist_4_Popularity', 'Artist_5_Popularity', 'Artist_6_Popularity']
	artist_values = {}
	for i in name_headers:
		iterate_csv(file_name, i)
		artist_values[i] = id_headers[i]
	
	return artists_values

#print(get_artists())

def main(file):
	with open('name_csv.csv', 'w', newline='', encoding='utf-7') as new_file:
		writer = csv.writer(new_file)

		headers = ['Artist_Name', 'Artist_Id']
		writer.writerow(headers)
		writer.writerows(get_artists(file))

		print("Success")

main('playlist.csv')

#So far this code fails... need to work on it
		








"""
Here I'm looking for the song in my playlist with the most artists
on it. This will help me figure out how many "artists" columns I'll
need to create when turning playlist.json into a csv file.
"""

import json

with open('playlist.json') as file:
    data = json.load(file)

items = data['items']

max_artist_count = 0
track_with_max_artists = None

for i in items:

    track = i['track']
    artists = track['artists']

    if len(artists) > max_artist_count:
        max_artist_count = len(artists)
        track_with_max_artists = track

print(f"{track_with_max_artists['name']} has the most artists with {max_artist_count} of them.")
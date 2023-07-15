"""Finds the song with the most artists singing on it.

Iterates through a json file of songs and for each song, and it counts how many
artists appear on the song.

As the script iterates through the json file, the track_with_max_artists variable
shows the song that currently has the most artists on it.

If another song has more artists, then track_with_max_artists equals the new song.
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
# Here's the big algorithm I'm writing to score a user's taste in music...
# It's gonan take a while to finish but I'll continue to push my code until it's done

import numpy as np
import csv
import pandas as pd
import math
import re

#Good -- returns DataFrame for csv file
def read_csv(file):
    df = pd.read_csv(file)
    return df

#Good -- returns dictionary of {artist name: weighted pop}
def weighted_artist_pop(csv_file):
    weighted_pop = {}
    avg = csv_file['Artist_Popularity'].mean()
    std = csv_file['Artist_Popularity'].std()

    for column in csv_file.columns:
        if column.startswith('Artist_Popularity'):
            for i, name in zip(csv_file[column], csv_file['Artist_Name']):
                z_score = (i - avg) / std
                new_score = (z_score * 20) + 50
                weighted_pop[name] = new_score
    
    return weighted_pop

#Good -- returns dictionary of {track name: weighted pop}
def weighted_track_pop(csv_file):
    weighted_pop = {}
    avg = csv_file['Track_Popularity'].mean()
    std = csv_file['Track_Popularity'].std()

    for column in csv_file.columns:
        if column.startswith('Track_Popularity'):
            for i, name in zip(csv_file[column], csv_file['Track_Name']):
                z_score = (i - avg) / std
                new_score = (z_score * 20) + 50
                weighted_pop[name] = new_score
    
    return weighted_pop

#Good -- returns dictionary of {artist name: place multiplier, artist 2 name: place multiplier, ...}
def artist_place(playlist, artist):
    playlist = playlist.fillna('')
    result = {}
    for i, p in playlist.iterrows():
        track_name = p['Track_Name']
        artist_pop = artist['Artist_Popularity']
        track = {}
        for j in playlist.columns:
            if j.endswith('1_Name'):
                a_name = p[j]
                if a_name != '':
                    track[p[j]] = 1
            elif j.endswith('2_Name'):
                a_name = str(p[j])
                if a_name != '':
                    track[p[j]] = 0.95
            elif j.endswith('3_Name'):
                a_name = p[j]
                if a_name != '':
                    track[p[j]] = 0.9
            elif j.endswith('4_Name'):
                a_name = p[j]
                if a_name != '':
                    track[p[j]] = 0.85
            elif j.endswith('5_Name'):
                a_name = p[j]
                if a_name != '':
                    track[p[j]] = 0.8
            elif j.endswith('6_Name'):
                a_name = p[j]
                if a_name != '':
                    track[p[j]] = 0.75

        result[track_name] = track
    return result


#Good -- returns dictionary of {Track_name: [list of featured artists]}
def featured_artist(playlist):
    featured_list = {}
    playlist = playlist[playlist['Track_Name'].str.contains('feat', case=False)]
    artist_names = ['Artist_1_Name','Artist_2_Name',
                    'Artist_3_Name','Artist_4_Name',
                    'Artist_5_Name','Artist_6_Name']


    for i, t in playlist.iterrows():
        track = t['Track_Name']
        feat = track.find('feat')
        after_feat = track[feat + len('feat'):]

        feat_artist = []
        for artist in artist_names:
            if str(t[artist]) in after_feat:
                feat_artist.append(t[artist])

        featured_list[t['Track_Name']] = feat_artist

    return featured_list

#Good -- returns dictionary of {artist: [top 10 tracks]}
def top_tracks(artist):
    result = {}
    
    for i, a in artist.iterrows():
        name = a['Artist_Name']
        top_tracks = []
        for j in artist.columns:
            if j.startswith('Top'):
                top_tracks.append(j)
        
        tracks = []
        for k in top_tracks:
            tracks.append(a[k])

        result[name] = tracks

    return result

#Good -- returns dictionary of {artist name: artist frequency}
def artists_frequency(playlist, artist):
    result = {}
    for a in artist.itertuples(index=False):
        count = 0
        for column in playlist.columns:
            if column.startswith('Artist_') and column.endswith('_Name'):
                for j in playlist[column]:
                    if j == a[0]:
                        count += 1
        result[a[0]] = count
    return result


def main(p, a):
    list_scores = []

    for i in p.columns:
        score = 0

    

    f_score = (sum(k for k in list_scores)/len(list_scores))
    return f_score


artist = read_csv('python_code/files/updated_artists.csv')
playlist = read_csv('python_code/files/playlist.csv')

# print(main('python_code/files/playlist.csv', 'python_code/files/updated_artists.csv'))
# print(weighted_artist_pop(artist))
# print(weighted_track_pop(playlist))
# print(artist_place(playlist, artist))
# print(featured_artist(playlist))
# print(top_tracks(artist))
# print(artists_frequency(playlist, artist))

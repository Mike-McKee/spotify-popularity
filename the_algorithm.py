# Here's the big algorithm I'm writing to score a user's taste in music...
# It's gonan take a while to finish but I'll continue to push my code until it's done

import numpy as np
import csv
import pandas as pd
import math

#Good
def read_csv(file):
    df = pd.read_csv(file)
    return df

#Good
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

#Good
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

#Good
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


#Needs Work
def featured_artist(playlist):
    featured_list = []
    track_name = playlist['Track_Name']
    artist_names = ['Artist_1_Name','Artist_2_Name',
                    'Artist_3_Name','Artist_4_Name',
                    'Artist_5_Name','Artist_6_Name']
    
    for i in track_name:
        if 'feat' in i or 'Feat' in i:
            for j in artist_names:
                for k in playlist[j]:
                    featured_list.append(k)

    return featured_list

#Good
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

# def main(playlist, artist):
#     score = []
#     p = read_csv(playlist)
#     a = read_csv(artist)

#     a_weight = weighted_artist_pop(a)
#     p_weight = weighted_track_pop(p)

#     for i in p:
#         temp = p_weight
        
#     return p

artist = read_csv('python_code/files/updated_artists.csv')
playlist = read_csv('python_code/files/playlist.csv')

# print(main('python_code/files/playlist.csv', 'python_code/files/updated_artists.csv'))
print(artist_place(playlist, artist))
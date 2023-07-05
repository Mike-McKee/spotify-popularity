# Here's the big algorithm I'm writing to score a user's taste in music...
# It's gonan take a while to finish but I'll continue to push my code until it's done

import numpy as np
import csv
import pandas as pd

def read_csv(file):
    df = pd.read_csv(file)
    return df

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

def artist_place(num):
    if num == 1:
        return 1
    elif num == 2:
        return 0.95
    elif num == 3:
        return 0.9
    elif num == 4:
        return 0.9
    elif num == 5:
        return 0.8
    elif num == 6:
        return 0.75

def featured_artist(name):
    if "feat" in name or "Feat" in name:
        return 0.5
    else:
        return 1

def top_tracks(artist):
    top_tracks = {}
    columns = []
    for i in artist.columns:
        if i.startswith('Top'):
            columns.append(i)
    for i in columns:
        top_tracks[artist['Artist_Name']] = artist[i]

    return top_tracks 

artist = read_csv('python_code/files/updated_artists.csv')
playlist = read_csv('python_code/files/playlist.csv')

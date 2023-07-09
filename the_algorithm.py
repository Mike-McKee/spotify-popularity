import numpy as np
import pandas as pd
import csv, math


# X defines how much we favor the popularity of the tracks compared to the artists popylarity
X = 2
Y = X + 1

# Returns DataFrame for csv file
def read_csv(file):
    df = pd.read_csv(file)
    return df

# Returns dictionary of {artist name: raw poplularity}
def raw_artists_pop(artist):
    raw_pop = {}
    for i, name in zip(artist['Artist_Popularity'], artist['Artist_Name']):
        raw_pop[name] = i
    return raw_pop

# Returns dictionary of {track name: raw popularity}
def raw_track_pop(playlist):
    raw_pop = {}
    for i, name in zip(playlist['Track_Popularity'], playlist['Track_Name']):
        raw_pop[name] = i
    return raw_pop        

# Returns dictionary of {artist name: weighted popularity}
def weighted_artist_pop(artist):
    weighted_pop = {}
    avg = artist['Artist_Popularity'].mean()
    std = artist['Artist_Popularity'].std()
    
    for i, name in zip(artist['Artist_Popularity'], artist['Artist_Name']):
        z_score = (i - avg) / std
        new_score = (z_score * 20) + 50
        weighted_pop[name] = new_score
    
    return weighted_pop

# Returns dictionary of {track name: weighted popularity}
def weighted_track_pop(playlist):
    weighted_pop = {}
    avg = playlist['Track_Popularity'].mean()
    std = playlist['Track_Popularity'].std()

    for i, name in zip(playlist['Track_Popularity'], playlist['Track_Name']):
        z_score = (i - avg) / std
        new_score = (z_score * 20) + 50
        weighted_pop[name] = new_score

    return weighted_pop

# Returns dictionary of {artist name: place multiplier, artist 2 name: place multiplier, ..., artist 6 name: place multiplier}
def artist_place(playlist, artist):
    playlist = playlist.fillna('')
    result = {}
    for i, p in playlist.iterrows():
        track_id = p['Track_Id']
        artist_pop = artist['Artist_Popularity']
        track = {}
        for j in playlist.columns:
            if j.endswith('1_Id'):
                a_id = p[j]
                if a_id != '':
                    track[p[j]] = 1
            elif j.endswith('2_Id'):
                a_id = str(p[j])
                if a_id != '':
                    track[p[j]] = 0.95
            elif j.endswith('3_Id'):
                a_id = p[j]
                if a_id != '':
                    track[p[j]] = 0.9
            elif j.endswith('4_Id'):
                a_id = p[j]
                if a_id != '':
                    track[p[j]] = 0.85
            elif j.endswith('5_Id'):
                a_id = p[j]
                if a_id != '':
                    track[p[j]] = 0.8
            elif j.endswith('6_Id'):
                a_id = p[j]
                if a_id != '':
                    track[p[j]] = 0.75

        result[track_id] = track
    return result

# Returns dictionary of {artist: [top 10 tracks]}
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

# Returns dictionary of {artist name: artist frequency}
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

# Returns dictionary of {artist: # of top tracks in playlist}
def percent_top_tracks(playlist, artist):
    result = {}

    for index, art in artist.iterrows():
        name = art['Artist_Name']
        tt = top_tracks(artist)[name]
        
        #counts how many of an artist's top tracks are in the playlist
        count = 0
        for track in tt:
            if track in playlist['Track_Name'].values:
                count += 1
        result[name] = count
    
    return result

# Returns dictionary {artist : multiplier based on ratio}
def track_ratio(playlist, artist):
    frequency = artists_frequency(playlist, artist)
    top_tracks_playlist = percent_top_tracks(playlist,artist)
    result = {}
    for i in frequency:
        ratio = top_tracks_playlist[i]/frequency[i]
        if ratio <= 0.25:
            result[i] = 0.85
        elif 0.25 < ratio <= 0.5:
            result[i] = 0.925
        elif 0.5 < ratio <= 0.75:
            result[i] = 1
        else:
            result[i] = 1.075

    return result            

#Solves equation using raw scores as base
def final_raw_score(playlist,artist):
    #removing null values
    playlist = playlist.fillna('')
    
    #Calling functions I'll need
    ra_pop = raw_artists_pop(artist)
    rt_pop = raw_track_pop(playlist)
    art_place = artist_place(playlist,artist)
    top_track = top_tracks(artist)
    artist_ratio = track_ratio(playlist,artist)

    #finds part 'r' of the equation
    raw = []
    for i in artist_ratio:
        raw.append(ra_pop[i] * artist_ratio[i])
    avg_raw = sum(raw)/len(raw)

    track_scores_raw = []
    for index, row in playlist.iterrows():
        artist_calc = []
        name = row['Track_Name']
        track_id = row['Track_Id']
        track_pop = rt_pop.get(name,0)
        a_place = art_place.get(track_id,0)

        for i in range(1,7):
            a_name = row[f'Artist_{i}_Name']
            a_id = row[f'Artist_{i}_Id']
            
            if a_name != '':
                a_pop = ra_pop.get(a_name,0)
                top_10 = top_track.get(a_name,0)

                #multiplier if song popularity < or > artists popularity
                multiplier = 0.9 if track_pop < a_pop else 1.1

                #multiplier if song is or is not in artist top tracks
                multiplier_2 = 1.1 if name in top_10 else 0.9

                #Finding the multiplier for artist place
                place = a_place[a_id]
                
                artist_calc.append(place*a_pop*(multiplier*multiplier_2))

        track_scores_raw.append((track_pop*len(artist_calc) + sum(artist_calc))/(len(artist_calc)+1))

    tr = sum(track_scores_raw)/len(track_scores_raw)

    return (X*tr + avg_raw)/Y

#Solves equation using weighted scores as base
def final_weighted_score(playlist,artist):
    #removing null values
    playlist = playlist.fillna('')
    
    #Calling functions I'll need
    wa_pop = weighted_artist_pop(artist)
    wt_pop = weighted_track_pop(playlist)
    art_place = artist_place(playlist,artist)
    top_track = top_tracks(artist)
    artist_ratio = track_ratio(playlist,artist)

    #finds part 'r' of the equation
    weighted = []
    for i in artist_ratio:
        weighted.append(wa_pop[i] * artist_ratio[i])
    avg_raw = sum(weighted)/len(weighted)

    track_scores_weighted = []
    for index, row in playlist.iterrows():
        artist_calc = []
        name = row['Track_Name']
        track_id = row['Track_Id']
        track_pop = wt_pop.get(name,0)
        a_place = art_place.get(track_id,0)

        for i in range(1,7):
            a_name = row[f'Artist_{i}_Name']
            a_id = row[f'Artist_{i}_Id']
            
            if a_name != '':
                a_pop = wa_pop.get(a_name,0)
                top_10 = top_track.get(a_name,0)

                #multiplier if song popularity < or > artists popularity
                multiplier = 0.9 if track_pop < a_pop else 1.1

                #multiplier if song is or is not in artist top tracks
                multiplier_2 = 1.1 if name in top_10 else 0.9

                #Finding the multiplier for artist place
                place = a_place[a_id]
                
                artist_calc.append(place*a_pop*(multiplier*multiplier_2))

        track_scores_weighted.append((track_pop*len(artist_calc) + sum(artist_calc))/(len(artist_calc)+1))

    tw = sum(track_scores_weighted)/len(track_scores_weighted)

    return (X*tw + avg_raw)/Y

#Calculates final score by averaging raw and weighted scores
def main(playlist,artist):
    return round((final_raw_score(playlist,artist) + final_weighted_score(playlist,artist))/2)
   

artist = read_csv('python_code/files/updated_artists.csv')
playlist = read_csv('python_code/files/playlist.csv')

print(main(playlist, artist))


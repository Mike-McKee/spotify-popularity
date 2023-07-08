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

# Returns dictionary of {artist name: place multiplier, artist 2 name: place multiplier, ...}
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


# Returns dictionary of {Track_name: [list of featured artists]}
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

#In progress
# def main(playlist,artist):
#     raw_scores = []
#     weighted_scores = []

#     ra_pop = raw_artists_pop(artist)
#     wa_pop = weighted_artist_pop(artist)
#     rt_pop = raw_track_pop(playlist)
#     wt_pop = weighted_track_pop(playlist)
#     art_place = artist_place(playlist,artist)
#     feat_artist = featured_artist(playlist)
#     top_track = top_tracks(artist)
#     artist_ratio = track_ratio(playlist,artist)

#     #finds part 'r' of the equation
#     raw = []
#     weight = []
#     for i in artist_ratio:
#         raw.append(ra_pop[i] * artist_ratio[i])
#         weight.append(wa_pop[i] * artist_ratio[i])
#     avg_raw = sum(raw)/len(raw)
#     avg_weight = sum(weight)/len(weight)
    

# artist = read_csv('python_code/files/updated_artists.csv')
# playlist = read_csv('python_code/files/playlist.csv')

# print(main(playlist, artist))

# print(main('python_code/files/playlist.csv', 'python_code/files/updated_artists.csv'))
# print(weighted_artist_pop(artist))
# print(weighted_track_pop(playlist))
# print(artist_place(playlist, artist))
# print(featured_artist(playlist))
# print(top_tracks(artist))
# print(artists_frequency(playlist, artist))
# print(raw_artists_pop(artist))
# print(raw_track_pop(playlist))
# print(percent_top_tracks(playlist, artist))
# print(track_ratio(playlist, artist))


#Testing how to use the functions in action
# place = artist_place(playlist,artist)
# weight = weighted_artist_pop(artist)
# raw = raw_artists_pop(artist)
# weighted = []
# raw_list = []
# for i in place:
#     for j in place[i]:
#         weighted.append(weight[j] * place[i][j])
#         raw_list.append(raw[j] * place[i][j])

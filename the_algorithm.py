"""
This script uses the data gathered and analyzed in other python scripts from
this project to score a Spotify user's taste in music.

It uses the equation defined here:
----------------------------------
https://github.com/Mike-McKee/spotify-popularity/blob/main/images/equation_w_annotations.png

"""
import pandas as pd

# X defines how much we favor the popularity of the tracks compared to the artists popylarity.
X = 2
Y = X + 1

def read_csv(file):
    """
    Uses pandas module to create a data frame with the file parameter.

    Parameter -- file
    -----------------
    - This has to be a csv file
    """

    df = pd.read_csv(file)
    return df

def artists_pop(artist):
    """
    Finds the artist popularity for all artists given in the parameter.

    Parameter -- DataFrame
    -------------------
    - artist is a Panda's DataFrame that's creaetd using the read_csv() function

    Return value -- dictionary
    --------------------------
    - Returns a dictionary in the format {artist name: arist popularity}

    Ex:
    {   
        'Abraham Mateo': 69,
        'Adam Levine': 71,
        'Aitana': 75,
        'Aleesha': 43,
        'Alejandro Rian1o': 31,
        'Alejandro Sanz': 75
    }
    """

    popularity = {}
    for i, name in zip(artist['Artist_Popularity'], artist['Artist_Name']):
        popularity[name] = i
    return popularity

def track_pop(playlist):
    """
    Finds the track popularity for all tracks given in the parameter.

    Parameter -- DataFrame
    -------------------
    - playlist is a Panda's DataFrame that's creaetd using the read_csv() function

    Return value -- dictionary
    --------------------------
    - Returns a dictionary in the format {track name: track popularity}

    Ex:
    {
        'Felices los 4': 77
        'ADMV': 72,
        'Chantaje (feat. Maluma)': 80,
        'Ignorantes': 72,
        'Me Gusta': 74,
        'Suerte (Whenever, Wherever)': 71
    }
    """

    popularity = {}
    for i, name in zip(playlist['Track_Popularity'], playlist['Track_Name']):
        popularity[name] = i
    return popularity        

def artist_place(playlist, artist):
    """
    Creates a scoring multiplier based on whether an artist is artist 1, 2, 3, 4, 5, or 6 on a track.
    The lower the artist place number, the higher the multiplier.

    Parameters -- DataFrame
    -----------------------
    - Playlist and artist are Panda's DataFrames created using read_csv()

    Return value -- Dictionary
    --------------------------
    - A dictionary in the following format is returned:
        
        {artist name: place multiplier, artist 2 name: place multiplier, ..., artist 6 name: place multiplier}
    
        The place multiplier options are the following:
            - Artist 1 = 1
            - Artist 2 = 0.95
            - Artist 3 = 0.9
            - Artist 4 = 0.85
            - Artist 5 = 0.8
            - Artist 6 = 0.75

    Ex:
    {
        '4TGwERXRlyQtBdggYTHo6j': {'5Y3MV9DZ0d87NnVm56qSY1': 1, '1vqR17Iv8VFdzure1TAXEq': 0.95, '1DxLCyH42yaHKGK3cl5bvG': 0.9, '2UZIAOlrnyZmyzt1nuXr9y': 0.85},
        '70LLyzO7jT6DsQvCwwHDch': {'1DxLCyH42yaHKGK3cl5bvG': 1},
        '0EhpEsp4L0oRGM0vmeaN5e': {'1vyhD5VmyZ7KMfW5gqLgo5': 1, '6M2wZ9GZgrQXHCFfjv46we': 0.95, '4q3ewBCX7sLwd24euuV69X': 0.9, '0GM7qgcRCORpGnfcN2tCiB': 0.85},
        '0gcOnIUKIG6JF56iFUfE0p': {'0UWZUmn7sybxMCqrw9tGa7': 1, '07YUOmWljBTXwIseAUd9TW': 0.95},
    }
    """
    
    playlist = playlist.fillna('')
    result = {}
    for i, p in playlist.iterrows():
        # Some songs have same track_name. So we iterate using track_id b/c it's a unique value
        track_id = p['Track_Id']

        #Can we remove artist_pop here?
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
    """
    Returns every artists' most popular songs.

    Parameter -- DataFrame
    ----------------------
    - artist is a Panda's DataFrame created using read_csv()


    Return value -- Dictionary
    --------------------------
    - A dictionary in the following format is returned:

        {artist: [top 10 tracks]}
    
    Ex:
    {
        'Abraham Mateo': ['Clavaito', 'Quiero Decirte', 'Te Miro A La Cara', "¿Qué Ha Pasao'?", 'Maníaca', 'Loco Enamorado', 'Bora Bora', 'La Idea', 'No Encuentro Palabras', 'Ahora Te Puedes Marchar'],
        'Adam Levine': ['Ojalá', 'Lost Stars', 'Lifestyle (feat. Adam Levine)', 'Good Mood - Original Song From Paw Patrol: The Movie', 'No One Else Like You', 'A Higher Place', 'Lifestyle (feat. Adam Levine) - David Guetta Slap House Mix', 'Lost Stars - Into The Night Mix', 'Yesterday - The Voice Performance', 'Wings Of Stone'], 'Aitana': ['Los Ángeles', 'Mon Amour - Remix', 'LAS BABYS', 'Presiento', 'Formentera', 'mariposas', 'Quieres', 'Vas A Quedarte', 'Más De Lo Que Aposté', 'En El Coche'], 'Aleesha': ['ESO', '828', 'Angelito', 'cómo t va?', 'Ke Sientes', 'Arrepentío', 'NO MAN', 'Sin Kerer', 'La Patrona', 'Tono de Llamada'], 'Alejandro Rian1o': ['Solo tú', nan, nan, nan, nan, nan, nan, nan, nan, nan],
        'Alejandro Sanz': ['La tortura', 'Corazón partío', 'Amiga mía', 'El Ultimo Adiós - Varios Artistas Version', 'Correcaminos', 'Mi soledad y yo', 'Te lo agradezco, pero no (feat. Shakira)', 'Un Beso en Madrid', 'Mi Persona Favorita', 'Desde cuando'],
        'Alejandro Valencia': ['Alma - Remix', 'MAMAXITA', 'CANSADA', 'SOLA', 'Pa Mi', 'Olvidate de El', nan, nan, nan, nan]
    }
    """

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

# Returns dictionary of 
def artists_frequency(playlist, artist):
    """
    Returns the number of times each artist appear on a playlist.

    Parameter -- DataFrame
    ----------------------
    - playlist and artist are Panda's DataFrames created using the read_csv() function

    Return value -- dictionary
    --------------------------
    - Returns a dictionary in the format {artist name: (int) artist frequency}
    
    Ex:
    {
    'Maluma': 48,
    'Manuel Turizo': 25,
    'Marc Anthony': 4,
    'Maria Becerra': 37,
    'Mariah Angeliq': 4,
    'Mariana Gomez': 1,
    'Matisse': 5,
    'Mau y Ricky': 18
    }
    """

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

def percent_top_tracks(playlist, artist):
    """
    Uses top_tracks() function to count how many of an artists top tracks appear
    in a playlist.

    Parameter -- DataFrame
    ----------------------
    - playlist and artist are Panda's DataFrames created using read_csv()

    Return value -- Dictionary
    --------------------------
    - A dictionary in the following format is returned:

        {artist: # of top tracks in playlist}
    
    Ex:
    {
     'Kevin Bury': 2,
     'Kewin Cosmos': 1,
     'Kim Loaiza': 1,
     'L-Gante': 1,
     'Lalo Ebratt': 3,
     'Lenny Tavarez': 3,
     'Lola Indigo': 2,
     'Maluma': 6,
     'Manuel Turizo': 5,
     'Marc Anthony': 1
    }
    """

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
    """
    Uses artists_frequency() and percent_top_tracks() functions to calculate
    every artists' ratio of "number of top songs in playlist to artist frequency".
    Using that ratio, the function assigns every artist a value between 0.85 and 1.075.

    Parameter -- DataFrame
    ----------------------
    - playlist and artist are Panda's DataFrames created using read_csv()

    Return value -- Dictionary
    --------------------------
    -- A dicitonary in the following format is returned:

        {artist : multiplier based on ratio}

    Ex:
    {
     'Myke Towers': 0.85,
     'Nacho': 0.925,
     'NATTI NATASHA': 0.85,
     'Nego do Borel': 0.85,
     'Nicki Minaj': 1.075,
     'Nicki Nicole': 0.925,
     'Nicky Jam': 0.85
    }

    """

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

#Solves equation to give final score
def final_score(playlist,artist):
    #removing null values
    playlist = playlist.fillna('')
    
    #Calling functions I'll need
    artist_pop = artists_pop(artist)
    track_popularity = track_pop(playlist)
    art_place = artist_place(playlist,artist)
    top_track = top_tracks(artist)
    artist_ratio = track_ratio(playlist,artist)

    #finds part 'r' of the equation
    ratio = []
    for i in artist_ratio:
        ratio.append(artist_pop[i] * artist_ratio[i])
    avg_ratio = sum(ratio)/len(ratio)

    track_scores = []
    for index, row in playlist.iterrows():
        artist_calc = []
        name = row['Track_Name']
        track_id = row['Track_Id']
        t_pop = track_popularity.get(name,0)
        a_place = art_place.get(track_id,0)

        for i in range(1,7):
            a_name = row[f'Artist_{i}_Name']
            a_id = row[f'Artist_{i}_Id']
            
            if a_name != '':
                a_pop = artist_pop.get(a_name,0)
                top_10 = top_track.get(a_name,0)

                #multiplier if song popularity < or > artists popularity
                multiplier = 0.9 if t_pop < a_pop else 1.1

                #multiplier if song is or is not in artist top tracks
                multiplier_2 = 1.1 if name in top_10 else 0.9

                #Finding the multiplier for artist place
                place = a_place[a_id]
                
                artist_calc.append(place*a_pop*(multiplier*multiplier_2))

        track_scores.append((t_pop*len(artist_calc) + sum(artist_calc))/(len(artist_calc)+1))

    tr = sum(track_scores)/len(track_scores)

    return (X*tr + avg_ratio)/Y


def main(playlist,artist):
    return round((final_score(playlist,artist)))
   

artist = read_csv('python_code/files/updated_artists.csv')
playlist = read_csv('python_code/files/playlist.csv')

print(main(playlist, artist))


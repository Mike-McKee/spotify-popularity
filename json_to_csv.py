import json
import csv

with open('playlist.json', 'r') as file:
    data = json.load(file)

t = data['items']
headers = ['Track_Name', 'Track_Id', 'Track_Popularity', 'Artist_1_Name', 'Artist_2_Name',
            'Artist_3_Name', 'Artist_4_Name', 'Artist_5_Name', 'Artist_6_Name',
            'Artist_1_Popularity', 'Artist_2_Popularity', 'Artist_3_Popularity',
            'Artist_4_Popularity', 'Artist_5_Popularity', 'Artist_6_Popularity']

with open('playlist.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    writer.writerow(headers)

    for i in t:
        track = i['track']

        track_name = track['name']
        track_id = track['id']
        track_pop = track['popularity']

        artist = track['artists']
        a_name = [] 
        a_id = []

        #iterates through all artists on a track and adds them to a list
        for i in artist:
            a_name.append(i['name'])
            a_id.append(i['id'])
    
        name_list = [""] * 6
        id_list = [""] * 6
        for i in range(len(a_name)):
            name_list[i] = a_name[i]
            id_list[i] = a_id[i]

        writer.writerow([track_name, track_id, track_pop] + name_list + id_list)

print("JSON turned into CSV: COMPLETE")

"""Cleaning the playlist.csv file and renaming some headers.

The os library is used for the following 3 actions:
---------------------------------------------------
1. Delete current csv file with wrong headers
2. Creates new csv file with the correct headers
3. Renames the new csv file to match the original file's name
"""

import os
import pandas as pd

df = pd.read_csv('files/playlist.csv')

df.rename(columns={
                    'Artist_1_Popularity': 'Artist_1_Id', 
                    'Artist_2_Popularity': 'Artist_2_Id',
                    'Artist_3_Popularity': 'Artist_3_Id',
                    'Artist_4_Popularity': 'Artist_4_Id',
                    'Artist_5_Popularity': 'Artist_5_Id',
                    'Artist_6_Popularity': 'Artist_6_Id'}, inplace=True)

df.to_csv('files/new_csv.csv', index=False)

os.remove('files/playlist.csv')
os.rename('files/new_csv.csv', 'files/playlist.csv')
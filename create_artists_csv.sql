# Using SQL and playlist.csv to create table we'll use to 
# get artist data from Spotify's API

SELECT Artist_1_Name AS 'Artist_Name', Artist_1_Popularity AS 'Artist_Id'
FROM playlist
WHERE Artist_1_Name <> ''
UNION
SELECT Artist_2_Name, Artist_2_Popularity
FROM playlist
WHERE Artist_2_Name <> ''
UNION
SELECT Artist_3_Name, Artist_3_Popularity
FROM playlist
WHERE Artist_3_Name <> ''
UNION
SELECT Artist_4_Name, Artist_4_Popularity
FROM playlist
WHERE Artist_4_Name <> ''
UNION
SELECT Artist_5_Name, Artist_5_Popularity
FROM playlist
WHERE Artist_5_Name <> ''
UNION
SELECT Artist_6_Name, Artist_6_Popularity
FROM playlist
WHERE Artist_6_Name <> ''
ORDER BY 1

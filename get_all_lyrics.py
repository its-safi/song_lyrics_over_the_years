# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 16:32:00 2021

@author: safiu
"""
import lyricsgenius as genius
import re
import pandas as pd
from datetime import datetime

all_song_lyrics = pd.DataFrame()
start_time = datetime.now()
print("Started at {}".format(start_time))

all_songs=pd.read_csv('all_songs.csv')

api_key = 'U96OEYnAWl7Kukp2CkILDHE5nQOuE9dsTAkQgO4U1_zAMwN1cZiPdbWoD2YWdISj'
api = genius.Genius(api_key, verbose = False)

for i in range(0, len(all_songs)):
    rolling_pct = int((i/len(all_songs))*100)
    print(str(rolling_pct) + "% complete." + " Collecting Record " + str(i) +" of " +
          str(len(all_songs)) +". Year " + str(all_songs.iloc[i]['Year']) + "." + " Currently collecting " + 
          all_songs.iloc[i]['Song Title'] + " by " + all_songs.iloc[i]['Artist'] + " "*50, end="\r")
    song_title = all_songs.iloc[i]['Song Title']
    song_title = re.sub(" and ", " & ", song_title)
    artist_name = all_songs.iloc[i]['Artist']
    artist_name = re.sub(" and ", " & ", artist_name)
    
    try:
        song = api.search_song(song_title, artist = artist_name)
        song_lyrics = re.sub("\n", " ", song.lyrics)

    except:
        song_lyrics = "null"
        
    row = {
        "Year": all_songs.iloc[i]['Year'],
        "Rank": all_songs.iloc[i]['Rank'],
        "Song Title": all_songs.iloc[i]['Song Title'],
        "Artist": all_songs.iloc[i]['Artist'],
        "Lyrics": song_lyrics,
    }
    
    all_song_lyrics = all_song_lyrics.append(row, ignore_index=True)


end_time = datetime.now()
print("\nCompleted at {}".format(start_time))
print("Total time to collect: {}".format(end_time - start_time))
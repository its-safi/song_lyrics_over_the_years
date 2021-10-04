# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 21:16:42 2021

@author: safiu
"""
import sys
import lyricsgenius as lg

api_key = "h261N9VMJIhwgV_5-MDZvUu96JiloOs_9Y-J6AM3ImSt5Zo9N-na9NUXHOGjqFFj"
genius = lg.Genius(api_key, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)

#Searches 5 of "Pop Smoke"'s songs via its Title.
artist = genius.search_artist("Pink Floyd",max_songs=1)

lyrics_song = artist.songs[0].lyrics

with open('lyr/prototype.txt', 'w', encoding='utf-8') as f:
    f.write(lyrics_song)
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 21:34:57 2021

@author: safiu
"""

import pandas as pd
import numpy as np
import sys
from bs4 import BeautifulSoup
import requests

def collect_songs_from_billboard(start_year,end_year):
    '''This function takes in a start year and and end year, then iterates through each year to 
    pull song data from billboard or bobborst as needed. Then it uses beautiful soup to clean
    the data. Finally it stores the cleaned data in a dataframe and returns it
    
    Parameters:
    
    start_year (int): the year to start at.
    end_year (int): the year to end at.
    Returns: 
    
    dataframe.
    '''
    
    years = np.arange(start_year, end_year + 1).astype(int)
    dataset = pd.DataFrame()
    url_list = []
    all_years = pd.DataFrame()
    ### Billboard doesn't have it's own complete results from 1970 to 2016,
    ### so we'll use bobborst.com as our primary and collect from billboard as needed
    alternate_site_collection_range = np.arange(start_year, 2017)
    #URL Constructor
    for i in range (0, len(years)):
        url_list.append("https://www.billboard.com/charts/year-end/" + str(years[i]) + "/hot-100-songs")      
    for i in range(0, len(url_list)):
            print("\r" + "Collecting Songs from " +str(years[i]) + " via https://www.billboard.com")
            url = "https://www.billboard.com/charts/year-end/" + str(years[i]) + "/hot-100-songs"
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            all_ranks = soup.find_all("div", class_="ye-chart-item__rank")
            all_titles = soup.find_all('div', class_="ye-chart-item__title")
            all_artists = soup.find_all("div", class_="ye-chart-item__artist")
            for j in range (0, len(all_ranks)):
                row = {
                    "Rank": all_ranks[j].get_text(strip=True),
                    "Song Title": all_titles[j].get_text(strip=True),
                    "Artist": all_artists[j].get_text(strip=True),
                    "Year": years[i]
                }
                dataset = dataset.append(row, ignore_index=True)
            import time
            time.sleep(20)
            print('len(all_ranks)')
    dataset['Year'] = dataset['Year'].astype(int)
    
    return dataset

all_songs = collect_songs_from_billboard(1970, 2020)
    
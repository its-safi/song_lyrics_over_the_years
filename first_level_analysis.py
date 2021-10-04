# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 22:23:35 2021

@author: safiu
"""

import pandas as pd
import numpy as np
import spacy
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import re


def plot_year_counts(dataset, X, y, title):
    '''Function to plot the year count summaries.
    
    Parameters:

    dataset (dataframe): pandas dataframe
    X (string): the x axis column
    y (string): the y axis column
    title (string): the title of the chart
    
    Outputs a matplotlib lineplot
    '''
    characteristics = dataset.groupby(X).count()
    mpl.rcParams['figure.figsize'] = (35,10,)
    #all_songs.groupby('Year').count().plot(kind='bar')
    sns.barplot(y=characteristics[y], x=characteristics.index)
    plt.title(title)
    plt.ylabel("Number of Songs")
    plt.xticks(rotation=90)
    

def add_spacy_data(dataset, feature_column):
    '''
    Grabs the verb, adverb, noun, and stop word Parts of Speech (POS) 
    tokens and pushes them into a new dataset. returns an 
    enriched dataset.
    
    Parameters:
    
    dataset (dataframe): the dataframe to parse
    feature_column (string): the column to parse in the dataset.
    
    Returns: 
    dataframe
    '''
    
    verbs = []
    nouns = []
    adverbs = []
    corpus = []
    nlp = spacy.load('en_core_web_sm')
    ##
    for i in range (0, len(dataset)):
        print("Extracting verbs and topics from record {} of {}".format(i+1, len(dataset)), end = "\r")
        song = dataset.iloc[i][feature_column]
        doc = nlp(song)
        spacy_dataframe = pd.DataFrame()
        for token in doc:
            if token.lemma_ == "-PRON-":
                    lemma = token.text
            else:
                lemma = token.lemma_
            row = {
                "Word": token.text,
                "Lemma": lemma,
                "PoS": token.pos_,
                "Stop Word": token.is_stop
            }
            spacy_dataframe = spacy_dataframe.append(row, ignore_index = True)
        verbs.append(" ".join(spacy_dataframe["Lemma"][spacy_dataframe["PoS"] == "VERB"].values))
        nouns.append(" ".join(spacy_dataframe["Lemma"][spacy_dataframe["PoS"] == "NOUN"].values))
        adverbs.append(" ".join(spacy_dataframe["Lemma"][spacy_dataframe["PoS"] == "ADV"].values))
        corpus_clean = " ".join(spacy_dataframe["Lemma"][spacy_dataframe["Stop Word"] == False].values)
        corpus_clean = re.sub(r'[^A-Za-z0-9]+', ' ', corpus_clean)   
        corpus.append(corpus_clean)
    dataset['Verbs'] = verbs
    dataset['Nouns'] = nouns
    dataset['Adverbs'] = adverbs
    dataset['Corpus'] = corpus
    return dataset   
all_songs_data=pd.read_csv('all_songs_lyrics.csv')
all_songs_data=all_songs_data[0:10]
loaded_song_dataset = pd.read_csv("all_songs_lyrics.csv",index_col=0)
loaded_song_dataset=loaded_song_dataset[0:10]
songs_with_lyrics_dataset = loaded_song_dataset.dropna(subset=['Lyrics'])

plot_year_counts(songs_with_lyrics_dataset, 'Year', 'Rank', 'Songs with Lyrics')



#Extracting Verbs , Nouns, and the Corpus

prepared_songs_dataset = add_spacy_data(songs_with_lyrics_dataset, 'Lyrics')
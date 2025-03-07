---
layout: post
title:  "Mapping Acoustic Evolution: A Data Dive into 1969 vs. 2019 Hits"
date: 2025-02-02
description: "Using APIs to look at 1969 and 2019 Billboard hits reveals a stark acoustic evolution—from raw guitar solos to algorithm-friendly synth drops—in this data-driven analysis of these musical eras."
image: "/assets/img/music_title.jpg"
---

## The Big Question
If you asked your parents for their taste in music, how would you say it differs from your own? What about if you asked your grandparents? In this analysis we look at data from both 1969 and 2019 to see how our music taste has changed throughout the decades.

**Prerequisites:** this post implies beginner/intermidiate level experience in python—specifically the pandas library—as well as a basic knowledge of how web scraping/APIs work. We will skip over some of the technicalities of certain functionality within Python as to provide a more generalized tutorial.

Here is a link to a Google Colab notebook with the code used in this tutorial: <a href="https://colab.research.google.com/drive/******************" target="_blank">Webscraping in Python</a>

**Learning Goals**

- The basics of API usage (particularly MusicBrainz and AcousticBrainz)
- How to set up a loop to collect a large dataset using an API
- How the most popular songs' acoustic features have changed since 1969

## Getting things ready

Here are the libraries we will be using:

```python
import pandas as pd
import requests
import datetime
import time
```

## What are people listening to?

To perform an analysis, we first need our data. For this we will be using first <a href="https://github.com/mhollingshead/billboard-hot-100/tree/main" target="_blank">This Github Repository</a>, which contains a dataset of the historic Billboard Hot 100 tracks since 1958. 

Let's load in the data and convert the date to datetime: 

```python
# get historic billboard data

url = 'https://raw.githubusercontent.com/mhollingshead/billboard-hot-100/main/all.json'

response = requests.get(url)
data = response.json()

billboard_df = pd.DataFrame(data)

billboard_df['date'] = pd.to_datetime(billboard_df['date'])
```

Now, we need to filter the data to only select the songs of 1969 as well as 2019, saving each dataframe as csv files for later use. Let's start with 2019:

```python
# filter data to only include dates from 2019

billboard_df_2019 = billboard_df[billboard_df['date'] >= datetime.datetime(2019, 1, 1)]
billboard_df_2019 = billboard_df_2019[billboard_df_2019['date'] <= datetime.datetime(2019, 12, 31)]

# unnest the data

billboard_df_2019 = billboard_df_2019['data'].explode().apply(pd.Series)

# convert last_week to int

billboard_df_2019['last_week'] = billboard_df_2019['last_week'].astype('Int64')

# save

billboard_df_2019.to_csv('billboard2019.csv', index = False)
```

Without loss of generality, the 1969 data is saved in the same manner. Note that we do not remove duplicates in this analysis, as we assume that a song being repeated on the Billboard Hot 100 is indicative of its popularity and enduring appeal.

Let's pick and compare the first two songs in each dataframe:

```python
print(f"2019: {billboard_df_2019['song'][0]} by {billboard_df_2019['artist'][0]}\n"
      f"1969: {billboard_df_1969['song'][0]} by {billboard_df_1969['artist'][0]}")
```

output: 
`2019: Thank U, Next by Ariana Grande
1969: I Heard It Through The Grapevine by Marvin Gaye`

Ah yes, one talking about their ex and the other of hearing rumors through the grapevine. Truly, the Billboard Hot 100 has always been the ultimate melting pot of everything gossip related!

## Using the MusicBrainz API

Now that we have our songs to analyze, we must uncover the acoustic features of each one. To do this, we will use a website called AcousticBrainz, which functions best when provided with a specific song ID (called an MBID). But first, we need to extract each song's MBID. Think of an MBID as a unique fingerprint for every song. With this fingerprint, we can then find then specific details pertaining to this individual song. To get these IDs, we will use a different website called MusicBrainz.

**Note:** It is important to always review API documentation, find the documentation for the MusicBrainz API <a href="https://musicbrainz.org/doc/Beginners_Guide" target="_blank">here</a>. Every API is different and had different syntax, requirements, and limitations.

First, we define a function to extract the MBID of any individual song.

```python
def get_recording_mbid(song, artist):
    # define our base url
    url = "https://musicbrainz.org/ws/2/recording"

    # query is what will be searched
    query = f'"{song}" by "{artist}"'

    params = {
        'query': query,
        'fmt': 'json',
        'limit': 1 # limit 1 indicates that we only want the first entry
        }

    headers = {
        # here you put the name of your application/purpose of API usage
        # as well as your email
        'User-Agent': 'DataAnalysis/1.0 (youremail@exampledomain.com)' 
        }
    
    try:
        response = requests.get( #get the data!!!
            url,
            params=params,
            headers=headers
            )
        # here we normalize our json output, selecting only the recording part of the multi-nested list, 
        # selecting the first element of the first list and only the 'id', this will give us the MBID
        return pd.json_normalize(response.json())['recordings'][0][0]['id']
    
    except: # in the case of an error, put a null value in the cell
        return None
```

Lets see how it works! `get_recording_mbid(billboard_df_2019['song'][0], billboard_df_2019['artist'][0])` gives us the MBID for "Thank U, Next" and outputs `274b3a7b-64bd-4af3-9af9-dd41277ddc17`. We will check the validity of this later.

With the function working, we create a for loop to extract the MBID of every individual song in both dataframes.

```python
for df in [billboard_df_2019, billboard_df_1969]: # looping through each df
    df['mbid'] = None # initializing mbid column
    
    for idx, row in df.iterrows(): # iterating through each row of df
        existing_mbids = df.loc[(df['song'] == row['song']) & (df['artist'] == row['artist']), 'mbid'] # check to see if already exists
    
        valid_mbids = existing_mbids[existing_mbids.apply(lambda x: len(x) == 36)] # check to see if valid mbid
    
        if not valid_mbids.empty: # if valid mbid already exists, paste existing mbid in cell
            df.at[idx, 'mbid'] = valid_mbids.iloc[0]
    
        else: # if no, use our function to get the mbid
            df.at[idx, 'mbid'] = get_recording_mbid(row['song'], row['artist'])
            time.sleep(1.5) # repeat every 1.5 seconds.
```

**Note: ** the MusicBrainz API has a rate limit of 10 requests per every 10 seconds, here we use a sleep timer of 1.5 just to be safe. Remember to not exceed the rate limit or you will be banned temporarily (or even permanently).


---
layout: post
title:  "Mapping Acoustic Evolution: A Data Dive into 1969 vs. 2019 Billboard Hot 100 Hits"
date: 2025-02-02
description: "Using APIs to look at 1969 and 2019 Billboard hits reveals a stark acoustic evolution—from raw guitar solos to algorithm-friendly synth drops—in this data-driven analysis of these musical eras."
image: "/assets/img/music_title.jpg"
---

## The Big Question
If you asked your parents for their taste in music, how would you say it differs from your own? What about if you asked your grandparents? In this analysis we look at data from both 1969 and 2019 to see how our music taste has changed throughout the decades.

**Prerequisites:** this post implies beginner/intermidiate level experience in python—specifically the pandas library—as well as a basic knowledge of how web scraping/APIs work. We will skip over a lot of the technicalities of certain functionality within Python in order to provide a more generalized tutorial. Note that the full extent of the code will be available in <a href="$#%#$%#$%#$%$" target="_blank">this GitHub repo</a> and in the provided Colab notebook as well.

Here is a link to a Google Colab notebook with the code used in this tutorial: <a href="https://colab.research.google.com/drive/******************" target="_blank">Webscraping in Python</a>

**Learning Goals**

- The basics of API usage (particularly MusicBrainz and AcousticBrainz)
- How to set up a loop to collect a large dataset using an API
- How the most popular songs' acoustic features have changed since 1969

## What are people listening to?

To perform an analysis, we first need our data. For this we will be using first <a href="https://github.com/mhollingshead/billboard-hot-100/tree/main" target="_blank">This Github Repository</a>, which contains a dataset of the historic Billboard Hot 100 tracks since 1958. 

After loading in the dataset, we then filter the data to only select the songs of 1969 as well as 2019, saving each dataframe as csv files for later use. Note that we do not remove duplicates in this analysis, as we assume that a song being repeated on the Billboard Hot 100 is indicative of its popularity and enduring appeal.

Let's pick and compare the first two songs in each dataframe:

```python
print(f"2019: {billboard_df_2019['song'][0]} by {billboard_df_2019['artist'][0]}\n"
      f"1969: {billboard_df_1969['song'][0]} by {billboard_df_1969['artist'][0]}")
```

output: 
`2019: Thank U, Next by Ariana Grande`
`1969: I Heard It Through The Grapevine by Marvin Gaye`

Ah yes, one talking about their ex and the other of hearing rumors through the grapevine. Truly, the Billboard Hot 100 has always been the ultimate melting pot of everything gossip related!

## Using the MusicBrainz API

Now that we have our songs to analyze, we must uncover the acoustic features of each one. To do this, we will use a website called AcousticBrainz, which functions best when provided with a specific song ID (called an MBID). But first, we need to extract each song's MBID. Think of an MBID as a unique fingerprint for every song. With this fingerprint, we can then find then specific details pertaining to this individual song. To get these IDs, we will use a different website called MusicBrainz. All we need to get started with using the API is the base url which I have provided, a 'query' which is essentially how we will look up each song, and our 'User-Agent' which is essentially identifying ourself to the website. Website owners like to know who is using their data.

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
        # as well as your email to identify who you are
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

Lets see how it works! `get_recording_mbid(billboard_df_2019['song'][0], billboard_df_2019['artist'][0])` gives us the MBID for "Thank U, Next" and outputs `274b3a7b-64bd-4af3-9af9-dd41277ddc17`.

With the function working, we can create a for loop to extract the MBID of every individual song in both dataframes.

**Note: ** the MusicBrainz API has a rate limit of 10 requests per every 10 seconds, in our code we use a sleep timer of 1.5 just to be safe. Remember to not exceed the rate limit or you will be banned temporarily (or even permanently).

## How to Use the AcousticBrainz API to Extract Song Features

Finally, we can start extracting the acoustic features of each individual song using the AcousticBrainz API. We define a function called `get_song_features`.While this is a lengthy function, the most important part to understand is that we take an MBID as our input, and we fetch the features based on their level using separate links. Low level features are more unambiguous such as key signature, BPM, while high level features are more up for interpretation. These could be things such as dancability, energy, or loudness. These features are being computed by a separate algorithm. Check the details for all features <a href="https://acousticbrainz.org/data" target="_blank">here</a>.

Let's check out the features for Mariah Carrey's 'All I Want For Christmas Is You':

```python
get_song_features(billboard_df_2019['mbid'][2])
```

`output: {'danceability': 'danceable', 'genre': 'pop', `
          `'gender': 'female', 'mood': 'not_aggressive', `
          `'instrumental': 'voice', 'bpm': 150.164459229, `
          `'key': 'G', 'loudness': 0.871298909187, `
          `'mood_happy': 'happy'}`

It seems fairly accurate, although I don't remember the song being particularly loud.

After defining the function, we need to loop through each data frame in order to retrieve the features of each song. What we need to do essentially is loop through the dataframe, running the get_song_features function to extract each row's features. Then, we assign each row's respective features to the corresponding column. An optimized version of this loop is included in the code.

Now we can save the results and analyze the data!

## How Have Songs Changed


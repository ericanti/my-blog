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

#save

billboard_df_2019.to_csv('billboard2019.csv', index = False)
```

Without loss of generality, the 1969 data is saved in the same manner. Note that we do not remove duplicates in this analysis, as we assume that a song being repeated on the Billboard Hot 100 is indicative of its popularity and enduring appeal.

Let's check to see what people were listening to 
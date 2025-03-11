import pandas as pd
import numpy as np
import requests
import datetime
import time
import matplotlib.pyplot as plt

# get historic billboard data

url = 'https://raw.githubusercontent.com/mhollingshead/billboard-hot-100/main/all.json'

response = requests.get(url)
data = response.json()

billboard_df = pd.DataFrame(data)

billboard_df['date'] = pd.to_datetime(billboard_df['date'])

# filter data to only include dates from 2019

billboard_df_2019 = billboard_df[billboard_df['date'] >= datetime.datetime(2019, 1, 1)]
billboard_df_2019 = billboard_df_2019[billboard_df_2019['date'] <= datetime.datetime(2019, 12, 31)]

# unnest the data

billboard_df_2019 = billboard_df_2019['data'].explode().apply(pd.Series)

# convert last_week to int

billboard_df_2019['last_week'] = billboard_df_2019['last_week'].astype('Int64')

#save

billboard_df_2019.to_csv('billboard2019.csv', index = False)

# filter data to only include dates between 1980 and 1990

billboard_df_1969 = billboard_df[billboard_df['date'] >= datetime.datetime(1969, 1, 1)]
billboard_df_1969 = billboard_df_1969[billboard_df_1969['date'] <= datetime.datetime(1969, 12, 31)]

# unnest the data

billboard_df_1969 = billboard_df_1969['data'].explode().apply(pd.Series)

# convert last_week to int

billboard_df_1969['last_week'] = billboard_df_1969['last_week'].astype('Int64')

#save

billboard_df_1969.to_csv('billboard1969.csv', index = False)

#testing
print(f"2019: {billboard_df_2019['song'][0]} by {billboard_df_2019['artist'][0]}\n"
      f"1969: {billboard_df_1969['song'][0]} by {billboard_df_1969['artist'][0]}")

# load in data

billboard_df_2019 = pd.read_csv('C:/Users/erica/STAT386/blog/another-stat386-theme/post2/billboard2019.csv')
billboard_df_1969 = pd.read_csv('C:/Users/erica/STAT386/blog/another-stat386-theme/post2/billboard1969.csv')

# fetch musicbrainz mbid

def get_recording_mbid(song, artist):
    url = "https://musicbrainz.org/ws/2/recording"

    query = f'"{song}" by "{artist}"'

    params = {
        'query': query,
        'fmt': 'json',
        'limit': 1
        }

    headers = {
        'User-Agent': 'DataAnalysis/1.0 (ericantilloncharles@gmail.com)'
        }
    
    try:

        response = requests.get(
            url,
            params=params,
            headers=headers
            )
        
        if response.status_code == 200:
            return pd.json_normalize(response.json())['recordings'][0][0]['id']
    
    except:
        return None
    
# testing

get_recording_mbid(billboard_df_2019['song'][0], billboard_df_2019['artist'][0])

# get mbids for both dataframes

for df in [billboard_df_2019, billboard_df_1969]:
    df['mbid'] = None
    
    for idx, row in df.iterrows():
        existing_mbids = df.loc[(df['song'] == row['song']) & 
                              (df['artist'] == row['artist']), 'mbid']
        
        valid_mbids = existing_mbids[existing_mbids.apply(
            lambda x: x is not None and len(x) == 36
        )]
        
        if not valid_mbids.empty:
            df.at[idx, 'mbid'] = valid_mbids.iloc[0]
        else:
            df.at[idx, 'mbid'] = get_recording_mbid(row['song'], row['artist'])
            time.sleep(1.5)

#filtering out null values and saving
billboard_df_2019 = billboard_df_2019[billboard_df_2019['mbid'].notnull()]
billboard_df_1969 = billboard_df_1969[billboard_df_1969['mbid'].notnull()]

billboard_df_2019.to_csv('billboard2019_mbid.csv', index = False)
billboard_df_1969.to_csv('billboard1969_mbid.csv', index = False)

# fetch acoustic features using acousticbrainz

# load data
billboard_df_2019 = pd.read_csv('C:/Users/erica/STAT386/blog/another-stat386-theme/post2/billboard2019_mbid.csv')
billboard_df_1969 = pd.read_csv('C:/Users/erica/STAT386/blog/another-stat386-theme/post2/billboard1969_mbid.csv')

def get_song_features(mbid):

    features = {
    'danceability': None,
    'genre': None,
    'gender': None,
    'mood': None,
    'instrumental': None,
    'bpm': None,
    'key': None,
    'loudness': None,
    'mood_happy': None
    }

    headers = {
        'User-Agent': 'DataAnalysis/1.0 (ericantilloncharles@gmail.com)'
        }

    # get high level and low level features

    try:

        hl_response = requests.get(
            f"https://acousticbrainz.org/api/v1/{mbid}/high-level",
            headers=headers
            )
        
        ll_response = requests.get(
            f"https://acousticbrainz.org/api/v1/{mbid}/low-level",
            headers=headers
            )
        
        # extract data

        if hl_response.status_code == 200 and ll_response.status_code == 200:
            hl_data = hl_response.json().get('highlevel', {})
            ll_data = ll_response.json()

            # update features

            features.update({
                'danceability': hl_data.get('danceability', {}).get('value'),
                'genre': hl_data.get('genre_rosamerica', {}).get('value'),
                'gender': hl_data.get('gender', {}).get('value'),
                'mood': hl_data.get('mood_aggressive', {}).get('value'),
                'instrumental': hl_data.get('voice_instrumental', {}).get('value'),
                'bpm': ll_data.get('rhythm', {}).get('bpm'),
                'key': ll_data.get('tonal', {}).get('key_key'),
                'loudness': ll_data.get('lowlevel', {}).get('average_loudness'),
                'mood_happy': hl_data.get('mood_happy', {}).get('value')
                })
            
            return features
    
    except:
        return None
    
get_song_features(billboard_df_2019['mbid'][2])
 
# create a cache to avoid unnecessary API calls
features_cache = {}

for df in [billboard_df_1969, billboard_df_2019]:
    for index, row in df.iterrows():
        mbid = row['mbid']
        
        if mbid in features_cache:
            # reuse cached features if applicable
            cached_features = features_cache[mbid]
            for feature in ['danceability', 'genre', 'gender', 'mood',
                            'instrumental', 'bpm', 'key', 'loudness', 'mood_happy']:
                df.at[index, feature] = cached_features.get(feature, None)
        else:
            # get features if not in cache
            song_features = get_song_features(mbid)

            if song_features:
                # cache the features
                features_cache[mbid] = song_features
                
                # assign features to the corresponding columns
                for feature in ['danceability', 'genre', 'gender', 'mood',
                                'instrumental', 'bpm', 'key', 'loudness', 'mood_happy']:
                    df.at[index, feature] = song_features.get(feature, None)
            else:
                # set all features to None if no data is found
                for feature in ['danceability', 'genre', 'gender', 'mood',
                                'instrumental', 'bpm', 'key', 'loudness', 'mood_happy']:
                    df.at[index, feature] = None

            # sleep for 3 seconds
            time.sleep(3)

# fill any duplicates that have null features
features = ['danceability', 'genre', 'gender', 'mood',
            'instrumental', 'bpm', 'key', 'loudness', 'mood_happy']

for df in [billboard_df_1969, billboard_df_2019]:
    needs_features = df['danceability'].isna()
    
    # Group by MBID and propagate features forward and backwards
    df.loc[needs_features, features] = df.groupby('mbid')[features].transform(
        lambda x: x.ffill().bfill()
    )

# filter only those with valid features
billboard_df_2019 = billboard_df_2019[billboard_df_2019['danceability'].notnull()]
billboard_df_1969 = billboard_df_1969[billboard_df_1969['danceability'].notnull()]

# save results
billboard_df_2019.to_csv('billboard2019_features.csv', index=False)
billboard_df_1969.to_csv('billboard1969_features.csv', index=False)

# load data
billboard_df_2019 = pd.read_csv('C:/Users/erica/STAT386/blog/another-stat386-theme/post2/billboard2019_features.csv')
billboard_df_1969 = pd.read_csv('C:/Users/erica/STAT386/blog/another-stat386-theme/post2/billboard1969_features.csv')

prop_happy_2019 = billboard_df_2019['mood_happy'].value_counts()['happy'] / billboard_df_2019['mood_happy'].value_counts().sum()
prop_not_happy_2019 = 1 - prop_happy_2019

prop_happy_1969 = billboard_df_1969['mood_happy'].value_counts()['happy'] / billboard_df_1969['mood_happy'].value_counts().sum()
prop_not_happy_1969 = 1 - prop_happy_1969

years = ['1969', '2019']
happy_proportions = [prop_happy_1969, prop_happy_2019]  # Proportion of happy songs
not_happy_proportions = [prop_not_happy_1969, prop_not_happy_2019]  # Proportion of not happy songs

# Create stacked bar plot
x = np.arange(len(years))  # Positions for bars
width = 0.5  # Width of bars

plt.bar(x, happy_proportions, width, label='Happy', color='yellow')
plt.bar(x, not_happy_proportions, width, bottom=happy_proportions, label='Not Happy', color='blue')

# Set x-axis labels
plt.xticks(x, years)

# Add a title and legend
plt.title('Proportion of Happy and Not Happy Songs by Year')
plt.legend()

# Display the plot
plt.show()

prop_male_2019 = billboard_df_2019['gender'].value_counts()['male'] / billboard_df_2019['gender'].value_counts().sum()
prop_female_2019 = billboard_df_2019['gender'].value_counts()['female'] / billboard_df_2019['gender'].value_counts().sum()

# Calculate proportions for gender in 1969
prop_male_1969 = billboard_df_1969['gender'].value_counts()['male'] / billboard_df_1969['gender'].value_counts().sum()
prop_female_1969 = billboard_df_1969['gender'].value_counts()['female'] / billboard_df_1969['gender'].value_counts().sum()

# Reverse the order of years and corresponding proportions
years = ['1969', '2019']
male_proportions = [prop_male_1969, prop_male_2019]
female_proportions = [prop_female_1969, prop_female_2019]

# Create stacked bar plot
x = np.arange(len(years))  # Positions for bars
width = 0.5  # Width of bars

plt.bar(x, male_proportions, width, label='Male', color='blue')
plt.bar(x, female_proportions, width, bottom=male_proportions, label='Female', color='pink')

# Set x-axis labels
plt.xticks(x, years)

# Add a title and legend
plt.title('Proportion of Male and Female Artists by Year')
plt.legend()

# Display the plot
plt.show()

billboard_df_2019[billboard_df_2019['peak_position'] == 1]['weeks_on_chart']

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 2019 Data
ax1.hist(billboard_df_2019[billboard_df_2019['peak_position'] == 1]['weeks_on_chart'], 
         bins=15, color='red', edgecolor='black', alpha=0.7, density=True)
ax1.set_title("Weeks on Chart for #1 Hits (2019)")
ax1.set_xlabel("Weeks on Chart")
ax1.set_ylabel("Density")
ax1.set_xlim(0, 55)  # Set x-axis limit to ensure consistent scale

# 1969 Data
ax2.hist(billboard_df_1969[billboard_df_1969['peak_position'] == 1]['weeks_on_chart'], 
         bins=15, color='blue', edgecolor='black', alpha=0.7, density=True)
ax2.set_title("Weeks on Chart for #1 Hits (1969)")
ax2.set_xlabel("Weeks on Chart")
ax2.set_ylabel("Density")
ax2.set_xlim(0, 55)  # Set x-axis limit to ensure consistent scale

# Adjust layout and show plot
plt.tight_layout()
plt.show()
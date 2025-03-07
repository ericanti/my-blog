import pandas as pd
import requests
import datetime
import time
from time import sleep
from urllib.parse import quote
from tqdm import tqdm

def get_billboard_data(url):
    response = requests.get(url)
    data = response.json()
    return data

my_url = 'https://raw.githubusercontent.com/mhollingshead/billboard-hot-100/main/all.json'
billboard_data = get_billboard_data(my_url)
billboard_df = pd.DataFrame(billboard_data)
billboard_df['date'] = pd.to_datetime(billboard_df['date'])

# filter data to only include dates from 1969
billboard_df_current = billboard_df[billboard_df['date'] >= datetime.datetime(2019, 1, 1)]
billboard_df_current = billboard_df_current[billboard_df_current['date'] <= datetime.datetime(2019, 12, 31)]

flattened_data = billboard_df_current['data'].explode().apply(pd.Series)

flattened_data['date'] = billboard_df_current.loc[flattened_data.index, 'date']

final_df_current = (flattened_data
            .set_index('song')
            .reset_index()[['song', 'date', 'artist', 'this_week', 
                           'last_week', 'peak_position', 'weeks_on_chart']]
           )

# convert non nan last_week to int

final_df_current['last_week'] = final_df_current['last_week'].fillna(pd.NA).astype('Int64')

# filter data to only include dates between 1980 and 1990

billboard_df_69 = billboard_df[billboard_df['date'] >= datetime.datetime(1969, 1, 1)]
billboard_df_69 = billboard_df_69[billboard_df_69['date'] <= datetime.datetime(1969, 12, 31)]

flattened_data = billboard_df_69['data'].explode().apply(pd.Series)

flattened_data['date'] = billboard_df_69.loc[flattened_data.index, 'date']

final_df_69 = (flattened_data
            .set_index('song')
            .reset_index()[['song', 'date', 'artist', 'this_week', 
                           'last_week', 'peak_position', 'weeks_on_chart']]
           )

# convert non nan last_week to int

final_df_69['last_week'] = final_df_69['last_week'].fillna(pd.NA).astype('Int64')

# fetch musicbrainz mbid

def get_recording_mbid(song, artist):
    base_url = "https://musicbrainz.org/ws/2/recording/"
    query = f'recording:"{song}" AND artist:"{artist}"'
    params = {
        'query': query,
        'fmt': 'json',
        'limit': 1
    }
    
    try:
        response = requests.get(
            base_url,
            params=params,
            headers={'User-Agent': 'DataAnalysis/1.0 (ericantilloncharles@gmail.com)'}  # Required by MB
        )
        response.raise_for_status()
        
        if response.json().get('recordings'):
            return response.json()['recordings'][0]['id']
        return None
    
    except Exception as e:
        print(f"Error for {song} by {artist}: {str(e)}")
        return None

for df in [final_df_current, final_df_69]:
    df['mbid'] = None
    
    for idx, row in df.iterrows():
        df.at[idx, 'mbid'] = get_recording_mbid(row['song'], row['artist'])
        sleep(1.1)

# filter only those with mbid

final_df_current = final_df_current[final_df_current['mbid'].notnull()]
final_df_69 = final_df_69[final_df_69['mbid'].notnull()]

final_df_current.to_csv('billboard_hot_100_2019.csv', index=False)
final_df_69.to_csv('billboard_hot_100_1969.csv', index=False)

# fetch acoustic features using acousticbrainz

# load data
final_df_69 = pd.read_csv('billboard_hot_100_1969.csv')
final_df_current = pd.read_csv('billboard_hot_100_2019.csv')

REQUEST_DELAY = 1.5  # Seconds between requests\
TIMEOUT = 10  # Seconds before request times outq
MAX_RETRIES = 3  # Maximum number of retries
USER_AGENT = 'DataAnalysis/1.0 (ericant@byu.edu)'

def create_feature_template():
    """Initialize all feature fields with None"""
    return {
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

def get_song_features(mbid, retry_count=0):
    """Get features for a single MBID with retry logic"""
    features = create_feature_template()
    
    try:
        # Combined endpoint attempt first
        response = requests.get(
            f"https://acousticbrainz.org/api/v1/{quote(mbid)}",
            headers={'User-Agent': USER_AGENT},
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            features.update({
                'danceability': data.get('highlevel', {}).get('danceability', {}).get('value'),
                'genre': data.get('highlevel', {}).get('genre_rosamerica', {}).get('value'),
                'gender': data.get('highlevel', {}).get('gender', {}).get('value'),
                'mood': data.get('highlevel', {}).get('mood_aggressive', {}).get('value'),
                'instrumental': data.get('highlevel', {}).get('voice_instrumental', {}).get('value'),
                'bpm': data.get('rhythm', {}).get('bpm'),
                'key': data.get('tonal', {}).get('key_key'),
                'loudness': data.get('lowlevel', {}).get('average_loudness')
            })
            return features
            
        # Fallback to individual endpoints if combined fails
        hl_response = requests.get(
            f"https://acousticbrainz.org/api/v1/{quote(mbid)}/high-level",
            headers={'User-Agent': USER_AGENT},
            timeout=TIMEOUT
        )
        ll_response = requests.get(
            f"https://acousticbrainz.org/api/v1/{quote(mbid)}/low-level",
            headers={'User-Agent': USER_AGENT},
            timeout=TIMEOUT
        )

        hl_data = hl_response.json().get('highlevel', {}) if hl_response.ok else {}
        ll_data = ll_response.json() if ll_response.ok else {}

        features.update({
            'danceability': hl_data.get('danceability', {}).get('value'),
            'genre': hl_data.get('genre_rosamerica', {}).get('value'),
            'gender': hl_data.get('gender', {}).get('value'),
            'mood': hl_data.get('mood_aggressive', {}).get('value'),
            'instrumental': hl_data.get('voice_instrumental', {}).get('value'),
            'bpm': ll_data.get('rhythm', {}).get('bpm'),
            'key': ll_data.get('tonal', {}).get('key_key'),
            'loudness': ll_data.get('lowlevel', {}).get('average_loudness'),
            'mood_happy': hl_data.get('mood_happy', {}).get('value'),
        })

    except requests.exceptions.RequestException as e:
        if retry_count < MAX_RETRIES:
            time.sleep(2 ** retry_count)  # Exponential backoff
            return get_song_features(mbid, retry_count + 1)
        print(f"Failed to retrieve {mbid} after {MAX_RETRIES} attempts")
        
    return features

get_song_features(final_df_69['mbid'].iloc[327])

for song in tqdm(final_df_69['mbid']):
    features = get_song_features(song)
    final_df_69.loc[final_df_69['mbid'] == song, 'danceability'] = features['danceability']
    final_df_69.loc[final_df_69['mbid'] == song, 'genre'] = features['genre']
    final_df_69.loc[final_df_69['mbid'] == song, 'gender'] = features['gender']
    final_df_69.loc[final_df_69['mbid'] == song, 'mood'] = features['mood']
    final_df_69.loc[final_df_69['mbid'] == song, 'instrumental'] = features['instrumental']
    final_df_69.loc[final_df_69['mbid'] == song, 'bpm'] = features['bpm']
    final_df_69.loc[final_df_69['mbid'] == song, 'key'] = features['key']
    final_df_69.loc[final_df_69['mbid'] == song, 'loudness'] = features['loudness']
    final_df_69.loc[final_df_69['mbid'] == song, 'mood_happy'] = features['mood_happy']
    sleep(REQUEST_DELAY)

for song in tqdm(final_df_current['mbid']):
    features = get_song_features(song)
    final_df_current.loc[final_df_current['mbid'] == song, 'danceability'] = features['danceability']
    final_df_current.loc[final_df_current['mbid'] == song, 'genre'] = features['genre']
    final_df_current.loc[final_df_current['mbid'] == song, 'gender'] = features['gender']
    final_df_current.loc[final_df_current['mbid'] == song, 'mood'] = features['mood']
    final_df_current.loc[final_df_current['mbid'] == song, 'instrumental'] = features['instrumental']
    final_df_current.loc[final_df_current['mbid'] == song, 'bpm'] = features['bpm']
    final_df_current.loc[final_df_current['mbid'] == song, 'key'] = features['key']
    final_df_current.loc[final_df_current['mbid'] == song, 'loudness'] = features['loudness']
    final_df_current.loc[final_df_current['mbid'] == song, 'mood_happy'] = features['mood_happy']
    sleep(REQUEST_DELAY)

# Save results
final_df_69.to_csv('billboard_hot_100_1969_features.csv', index=False)
final_df_current.to_csv('billboard_hot_100_2019_features.csv', index=False)
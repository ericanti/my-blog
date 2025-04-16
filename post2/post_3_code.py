import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# load the datasets
billboard_df_2019 = pd.read_csv('C:/Users/erica/STAT386/blog/another-stat386-theme/post2/billboard2019_features.csv')
billboard_df_1969 = pd.read_csv('C:/Users/erica/STAT386/blog/another-stat386-theme/post2/billboard1969_features.csv')

# add year column to each dataframe
billboard_df_2019['Year'] = 2019
billboard_df_1969['Year'] = 1969

# merge the dataframes
merged_data = pd.concat([billboard_df_2019, billboard_df_1969])

# EDA -----------------------------------------------------------------

# comparing happy vs non-happy songs
prop_happy_2019 = billboard_df_2019['mood_happy'].value_counts()['happy'] / billboard_df_2019['mood_happy'].value_counts().sum()
prop_not_happy_2019 = 1 - prop_happy_2019

prop_happy_1969 = billboard_df_1969['mood_happy'].value_counts()['happy'] / billboard_df_1969['mood_happy'].value_counts().sum()
prop_not_happy_1969 = 1 - prop_happy_1969

years = ['1969', '2019']
happy_proportions = [prop_happy_1969, prop_happy_2019]
not_happy_proportions = [prop_not_happy_1969, prop_not_happy_2019]

data = pd.DataFrame({
    'Year': years + years,
    'Proportion': happy_proportions + not_happy_proportions,
    'Mood': ['Happy'] * 2 + ['Not Happy'] * 2
})

pastel_orange = '#FFC499'
pastel_blue = '#87CEEB'

sns.set_style("whitegrid")
sns.set_palette([pastel_orange, pastel_blue])

plt.figure(figsize=(10, 6))
sns.barplot(x='Year', y='Proportion', hue='Mood', data=data)

plt.title('Proportion of Happy and Not Happy Songs by Year', fontsize=16, pad=20)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Proportion', fontsize=12)
plt.legend(title='Mood', title_fontsize='12', fontsize='10')

plt.tight_layout()

plt.show()

# comparing proportion of male vs female artists
prop_male_2019 = billboard_df_2019['gender'].value_counts()['male'] / billboard_df_2019['gender'].value_counts().sum()
prop_female_2019 = 1 - prop_male_2019

prop_male_1969 = billboard_df_1969['gender'].value_counts()['male'] / billboard_df_1969['gender'].value_counts().sum()
prop_female_1969 = 1 - prop_male_1969

years = ['1969', '2019']
male_proportions = [prop_male_1969, prop_male_2019]
female_proportions = [prop_female_1969, prop_female_2019]

data = pd.DataFrame({
    'Year': years + years,
    'Proportion': male_proportions + female_proportions,
    'Gender': ['Male'] * 2 + ['Female'] * 2
})

pastel_red = '#FFB6C1'
pastel_blue = '#87CEEB'

sns.set_style("whitegrid")
sns.set_palette([pastel_blue, pastel_red])

plt.figure(figsize=(10, 6))
sns.barplot(x='Year', y='Proportion', hue='Gender', data=data)

plt.title('Proportion of Male and Female Artists by Year', fontsize=16, pad=20)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Proportion', fontsize=12)
plt.legend(title='Gender', title_fontsize='12', fontsize='10')

plt.tight_layout()

plt.show()

# comparing longevity of #1 songs between years
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

bin_edges = np.linspace(0, 60, 11)

# filter for songs in the top 5 and select the week with the highest 'weeks_on_chart'
top_5_1969 = (
    billboard_df_1969[billboard_df_1969['peak_position'].between(1, 5)]
    .sort_values('weeks_on_chart', ascending=False)
    .drop_duplicates(subset='mbid')  # keep only the row with max weeks_on_chart per song
)

top_5_2019 = (
    billboard_df_2019[billboard_df_2019['peak_position'].between(1, 5)]
    .sort_values('weeks_on_chart', ascending=False)
    .drop_duplicates(subset='mbid')
)

ax1.hist(top_5_1969['weeks_on_chart'], 
         bins=bin_edges, color='blue', edgecolor='black', alpha=0.7, density=True)
ax1.set_title("Weeks on Chart for Top 5 Songs (1969)")
ax1.set_xlabel("Weeks on Chart")
ax1.set_ylabel("Density")
ax1.set_xlim(0, 60)
ax1.set_ylim(0, 0.15)

ax2.hist(top_5_2019['weeks_on_chart'], 
         bins=bin_edges, color='red', edgecolor='black', alpha=0.7, density=True)
ax2.set_title("Weeks on Chart for Top 5 Songs (2019)")
ax2.set_xlabel("Weeks on Chart")
ax2.set_ylabel("Density")
ax2.set_xlim(0, 60)
ax2.set_ylim(0, 0.15)

plt.tight_layout()

plt.show()

# Define mapping from genre codes to full names
genre_label_map = {
    'cla': 'Classical',
    'dan': 'Dance/Electronic',
    'hip': 'Hip-Hop',
    'jaz': 'Jazz',
    'pop': 'Pop',
    'rhy': 'Rhythm & Blues (R&B)',
    'roc': 'Rock',
    'spe': 'Speech'
}

# Add a new column with the full genre names
billboard_df_1969['genre_full'] = billboard_df_1969['genre'].map(genre_label_map).fillna(billboard_df_1969['genre'])
billboard_df_2019['genre_full'] = billboard_df_2019['genre'].map(genre_label_map).fillna(billboard_df_2019['genre'])

# Calculate genre proportions for each year using the new full label column
genre_1969 = billboard_df_1969['genre_full'].value_counts(normalize=True).reset_index()
genre_1969.columns = ['Genre', 'Proportion']
genre_1969['Year'] = '1969'

genre_2019 = billboard_df_2019['genre_full'].value_counts(normalize=True).reset_index()
genre_2019.columns = ['Genre', 'Proportion']
genre_2019['Year'] = '2019'

# Combine for plotting
genre_df = pd.concat([genre_1969, genre_2019], ignore_index=True)

# Set color palette
pastel_green = '#A8E6CF'
pastel_purple = '#B39DDB'
sns.set_palette([pastel_green, pastel_purple])
sns.set_style("whitegrid")

plt.figure(figsize=(12, 7))
sns.barplot(x='Genre', y='Proportion', hue='Year', data=genre_df)

plt.title('Genre Distribution by Year', fontsize=16, pad=20)
plt.xlabel('Genre', fontsize=12)
plt.ylabel('Proportion', fontsize=12)
plt.legend(title='Year', title_fontsize='12', fontsize='10')
plt.xticks(rotation=30, ha='right')

plt.tight_layout()
plt.savefig('genre_distribution.png', dpi=300, bbox_inches='tight')
plt.show()
import pandas as pd

song_features = pd.read_csv('../data/merged_v3.csv')

columns_to_impute = ['song_popularity', 'song_danceability', 'song_energy', 'song_key', 'song_loudness', 'song_mode',
                     'song_speechiness', 'song_acousticness', 'song_instrumentalness', 'song_liveness', 'song_valence',
                     'song_tempo', 'song_duration_ms', 'song_time_signature']

song_features_to_clean = song_features[song_features['song_popularity'].isnull()]

count = 0
for index, row in song_features.iterrows():
    if not pd.notnull(row['song_popularity']):
        print("Imputing for " + row['title'] + ' ' + row['artist'])
        artist_songs = song_features[(song_features['artist'] == row['artist']) & (pd.notnull(row['song_popularity']))]
        if artist_songs.shape[0] > 0:
            for column in columns_to_impute:
                song_features.at[index, column] = artist_songs[column].mean()
        else:
            year_songs = song_features[song_features['release_year'] == row['release_year']]
            year_songs = year_songs.dropna()
            for column in columns_to_impute:
                song_features.at[index, column] = year_songs[column].mean()

song_features.to_csv('../data/merged_v3_cleaned.csv')

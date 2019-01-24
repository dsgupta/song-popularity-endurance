import pandas as pd

billboard_df = pd.read_csv('../data/billboard_100.csv')
lastfm_df = pd.read_csv('../data/last_fm_hot100_final.csv')
spotify_df = pd.read_csv('../data/spotify.csv', encoding="ISO-8859-1")
billboard_info_df = pd.read_csv('../data/billboard_info_v3.csv')

merged_df = pd.DataFrame()

lastfm_columns = lastfm_df.columns.values.tolist()
spotify_columns = spotify_df.columns.values.tolist()

print(lastfm_columns)
print(spotify_columns)

lastfm_merged = lastfm_df.groupby(['title', 'artist'], as_index=False).agg({'listeners': sum,
                                                                            'playcount': sum})

billboard_df['title_artist'] = billboard_df['title'] + '~' + billboard_df['artist']
billboard_info_df['title_artist'] = billboard_info_df['title'] + '~' + billboard_info_df['artist']
spotify_df['artist'] = spotify_df['artist'].map(lambda x: x.lstrip('b\'').rstrip('\''))
spotify_df['title_artist'] = spotify_df['title'] + '~' + spotify_df['artist']
lastfm_merged['title_artist'] = lastfm_merged['title'] + '~' + lastfm_merged['artist']
merged_df = billboard_df.merge(spotify_df, left_on='title_artist', right_on='title_artist',
                               how='left')
merged_df = merged_df.merge(lastfm_merged, left_on='title_artist', right_on='title_artist',
                            how='left')

merged_df = merged_df.merge(billboard_info_df, left_on='title_artist', right_on='title_artist',
                            how='left')

merged_df.to_csv('../data/merged_v3.csv')

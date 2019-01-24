import pandas as pd
from datetime import datetime as dt
import datetime
import numpy as np

songs_df = pd.read_csv('/Users/sayakghosh/Documents/sem1/dsf/project/data-scrapers/merged.csv')
billboard_df = pd.read_csv('/Users/sayakghosh/Documents/sem1/dsf/project/data-scrapers/billboard_3.csv')

billboard_info = pd.DataFrame()
errors = pd.DataFrame()


def calculate_year_difference(last_date, first_date):
    d1 = dt.strptime(str(last_date).rstrip('\\n'), "%Y-%m-%d")
    d2 = dt.strptime(str(first_date), "%Y-%m-%d")
    return abs((d1 - d2).days / 365.0)


def calculate_day_difference(first_date, last_date):
    return abs((last_date - first_date).days)


def calculate_max_run(billboard_rows):
    max_run = 1
    current_run = 1
    for index, row in billboard_rows.iterrows():
        if calculate_day_difference(row['date'], row['next_date']) == 7:
            current_run = current_run + 1
            if (current_run > max_run):
                max_run = current_run
            else:
                current_run = 1
    return max_run


def derive_billboard_features(df):
    weeks_in_billboard = df['artist'].count()
    max_run = calculate_max_run(df)
    weeks_in_top_ten = df[df['rank'] <= 10]['rank'].count()
    weeks_in_top_thirty = df[df['rank'] <= 30][
        'rank'].count()
    weeks_in_top_fifty_ = df[df['rank'] <= 50][
        'rank'].count()
    best_rank = df['rank'].min()
    worst_rank = df['rank'].max()
    average_rank = df['rank'].mean()
    rank_change = df.tail(1)['rank'].values[0] - \
                  df.head(1)['rank'].values[0]

    return weeks_in_billboard, max_run, weeks_in_top_ten, weeks_in_top_thirty, weeks_in_top_fifty_, best_rank, worst_rank, average_rank, rank_change


for index, row in songs_df.iterrows():
    billboard_rows = pd.DataFrame()
    billboard_info_row = pd.DataFrame()
    try:
        billboard_rows = billboard_df[
            (billboard_df['title'] == row['title_x']) & (billboard_df['artist'] == row['artist_x'])]
        print("Aggregating for " + row['title_x'] + " " + row['artist_x'])
        billboard_rows['date'] = billboard_rows['date'].map(
            lambda x: dt.strptime(str(x).rstrip('\\n'), "%Y-%m-%d"))
        billboard_rows['next_date'] = billboard_rows['date'].shift(-1)

        weeks_in_billboard = billboard_rows['artist'].count()
        max_run = calculate_max_run(billboard_rows)
        weeks_in_top_ten = billboard_rows[billboard_rows['rank'] <= 10]['rank'].count()
        weeks_in_top_thirty = billboard_rows[billboard_rows['rank'] <= 30]['rank'].count()
        weeks_in_top_fifty = billboard_rows[billboard_rows['rank'] <= 50]['rank'].count()

        first_date = billboard_rows.tail(1)['date'].to_string().split(' ')[
            len(billboard_rows.tail(1)['date'].to_string().split(' ')) - 1]

        first_year = dt.strptime(str(first_date).rstrip('\\n'), "%Y-%m-%d")
        release_year = first_year.year
        first_year_end = first_year + datetime.timedelta(days=(1 * 365))
        twenty_year_end = first_year + datetime.timedelta(days=(20 * 365))

        billboard_info_first_year = billboard_rows[billboard_rows['date'] <= first_year_end]
        billboard_info_twenty_years = billboard_rows[billboard_rows['date'] <= twenty_year_end]

        ###First Year Metrics

        weeks_in_billboard_first_year, max_run_first_year, weeks_in_top_ten_first_year, weeks_in_top_thirty_first_year, weeks_in_top_fifty_first_year, best_rank_first_year, worst_rank_first_year, average_rank_first_year, first_year_rank_change = derive_billboard_features(
            billboard_info_first_year)
        ###Twenty Year Metrics

        weeks_in_billboard_twenty_year, max_run_twenty_year, weeks_in_top_ten_twenty_year, weeks_in_top_thirty_twenty_year, weeks_in_top_fifty_twenty_year, best_rank_twenty_years, worst_rank_twenty_years, average_rank_twenty_years, twenty_year_rank_change = derive_billboard_features(
            billboard_info_twenty_years)

        last_date = billboard_rows.head(1)['date'].to_string().split(' ')[
            len(billboard_rows.tail(1)['date'].to_string().split(' ')) - 1]

        years = calculate_year_difference(last_date, first_date)

        release_date = np.nan
        try:
            release_date = dt.strptime(str(row['release_date']), "%m/%d/%Y").strftime('%Y-%m-%d')
        except:
            print("Release date not present")

        billboard_info = billboard_info.append(
            {'title': row['title_x'], 'artist': row['artist_x'], 'release_date': release_date,
             'weeks_in_billboard': weeks_in_billboard,
             'average_rank_in_billboard': billboard_rows['rank'].mean(),
             'best_rank': billboard_rows['rank'].min(), 'worst_rank': billboard_rows['rank'].max(),
             'first_date': first_date, 'last_date_in_billboard': last_date,
             'year_range_billboard': years, 'max_run': max_run, 'weeks_in_top_ten': weeks_in_top_ten,
             'weeks_in_top_thirty': weeks_in_top_thirty, 'weeks_in_top_fifty': weeks_in_top_fifty,
             'weeks_in_billboard_first_year': weeks_in_billboard_first_year, 'max_run_first_year': max_run_first_year,
             'weeks_in_top_ten_first_year': weeks_in_top_ten_first_year,
             'weeks_in_top_thirty_first_year': weeks_in_top_thirty_first_year,
             'weeks_in_top_fifty_first_year': weeks_in_top_fifty_first_year,
             'best_rank_in_first_year': best_rank_first_year, 'worst_rank_first_year': worst_rank_first_year,
             'average_rank_first_year': average_rank_first_year, 'first_year_rank_change': first_year_rank_change,
             'weeks_in_billboard_twenty_years': weeks_in_billboard_twenty_year,
             'max_run_twenty_year': max_run_twenty_year,
             'weeks_in_top_ten_twenty_years': weeks_in_top_ten_twenty_year,
             'weeks_in_top_thirty_twenty_years': weeks_in_top_thirty_twenty_year,
             'weeks_in_top_fifty_twenty_years': weeks_in_top_fifty_twenty_year,
             'best_rank_in_twenty_years': best_rank_twenty_years, 'worst_rank_twenty_year': worst_rank_twenty_years,
             'average_rank_twenty_years': average_rank_twenty_years, 'twenty_year_rank_change': twenty_year_rank_change,
             'release_year': release_year
             },
            ignore_index=True)
    except:
        errors = errors.append({'title': row['title_x'], 'artist': row['artist_x']}, ignore_index=True)

billboard_info.to_csv('../data/billboard_info_v3.csv', index=False)
errors.to_csv('../data/error_billboard_aggregate_v3.csv',
              index=False)

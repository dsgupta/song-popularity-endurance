import pandas as pd
import asyncio
from aiohttp import ClientSession
from aiohttp import TCPConnector
import requests
import json
import re

lastfm_df = pd.DataFrame()
error_df = pd.DataFrame()
hits = []
errors = []


def get_url(row):
    urls = []
    base_url = 'http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=8aa30acda35f78c51911a8c5e165767a&artist='
    urls.append(base_url + str(row.artist) + '&track=' + str(row.title) + '&format=json')
    if 'Featuring' in row.artist:
        sanitized_artist_name = re.sub("\(Featuring", "Featuring", row.artist)
        try:
            tokens = sanitized_artist_name.split(' ')
            index = tokens.index('Featuring')
            tokens = tokens[:index]
            new_artist = ''
            for token in tokens:
                new_artist = new_artist + token + ' '
            new_artist = new_artist.rstrip()
            urls.append(base_url + str(new_artist) + '&track=' + str(row.title) + '&format=json')
        except ValueError:
            print("Exception in parsing artist" + row.artist)
    return urls


async def make_requests(row):
    urls = get_url(row)
    connector = TCPConnector(limit=2)
    asyncio.sleep(1)
    async with ClientSession(connector=connector) as session:
        for url in urls:
            async with session.get(url) as response:
                response = await response.json()
                if ('track' in response.keys()):
                    print(response)
                    hits.append(
                        {'title': row.title, 'artist': row.artist, 'listeners': response['track']['listeners'],
                         'playcount': response['track']['playcount'], 'durations': response['track']['duration']})


df = pd.read_csv('../data/last_fm_input.csv')

# loop = asyncio.get_event_loop()
# tasks = []
#
# for _, row in df.iterrows():
#     task = asyncio.ensure_future(make_requests(row))
#     tasks.append(task)
# loop.run_until_complete(asyncio.wait(tasks))


for _, row in df.iterrows():
    urls = get_url(row)
    for url in urls:
        try:
            response = requests.get(url=url).json()
            if ('track' in response.keys()):
                print(response)
                hits.append(
                    {'title': row.title, 'artist': row.artist, 'listeners': response['track']['listeners'],
                     'playcount': response['track']['playcount'], 'durations': response['track']['duration']})
            else:
                errors.append({'title': row.title, 'artist': row.artist})

        except json.decoder.JSONDecodeError:
            errors.append({'title': row.title, 'artist': row.artist})

lastfm_df = lastfm_df.append(hits, ignore_index=True)
error_df = error_df.append(errors, ignore_index=True)
lastfm_df.to_csv('/Users/sayakghosh/Documents/sem1/dsf/project/data-scrapers/last_fm_hot100_2.csv')
error_df.to_csv('/Users/sayakghosh/Documents/sem1/dsf/project/data-scrapers/last_fm_errors_2.csv')

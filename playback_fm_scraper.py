from requests import get
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://playback.fm/year/1960'

hits = []

df = pd.DataFrame()


def getUrls():
    urls = []
    base_url = 'https://playback.fm/year/'
    for i in range(1950, 2017):
        url = base_url + str(i)
        urls.append(url)
    return urls


urls = getUrls()


def getYear(url):
    tokens = url.split('/')
    length = len(tokens)
    return tokens[length - 1]


for url in urls:
    response = get(url)
    year = getYear(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    song_containers = html_soup.find_all('tr', class_='playlistItem')
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    song_containers = html_soup.find_all('tr', class_='playlistItem')

    for song_container in song_containers:
        print(song_container)
        inputs = song_container.find_all('input')
        outputs = []
        for input in inputs:
            outputs.append(input['value'])
        hits.append(
            {'title': outputs[2], 'artist': outputs[1], 'rank': outputs[3], 'youtubeId': outputs[0], 'year': year})

df = df.append(hits, ignore_index=True)
df.to_csv('../data/playback_fm.csv')


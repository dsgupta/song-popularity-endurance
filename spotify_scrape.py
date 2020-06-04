# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 16:54:57 2018

@author: damay
"""
import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import json
import pandas as pd
from time import sleep
import csv
import re

memo = {}
def refresh():
    global memo
    memo = {}

def levenshtein(s, t):
    if s == "":
        return len(t)
    if t == "":
        return len(s)
    cost = 0 if s[-1] == t[-1] else 1

    i1 = (s[:-1], t)
    if not i1 in memo:
        memo[i1] = levenshtein(*i1)
    i2 = (s, t[:-1])
    if not i2 in memo:
        memo[i2] = levenshtein(*i2)
    i3 = (s[:-1], t[:-1])
    if not i3 in memo:
        memo[i3] = levenshtein(*i3)
    res = min([memo[i1]+1, memo[i2]+1, memo[i3]+cost])

    return res



df = pd.read_csv(r'D:\Documents\Data Science\DSF Project\billboard_100.csv')
output = open(r'D:\Documents\Data Science\DSF Project\bill_spot_100_abc1.csv', mode='w', newline='')
error = open(r'D:\Documents\Data Science\DSF Project\error_100_abc1.csv', mode='w', newline='')
fields=['title', 'artist', 'album_name','total_tracks','release_date','album_popularity',
        'label','is_explicit', 'genre', 'artist_popularity', 'song_popularity', 'song_danceability','song_energy','song_key',
        'song_loudness','song_mode','song_speechiness','song_acousticness',
        'song_instrumentalness','song_liveness','song_valence','song_tempo',
        'song_duration_ms','song_time_signature']

dw = csv.DictWriter(output,fieldnames=fields)
dw.writeheader()
err = csv.writer(error, delimiter=',')
token = util.oauth2.SpotifyClientCredentials(client_id='xxx',
                                                      client_secret='yyy')
cache_token = token.get_access_token()
sp = spotipy.Spotify(cache_token)
for i, row in df.iterrows():
    refresh()
    song = {}
    sleep(0.05)
    title =  row['title']
    artist = row['artist']
    artist = row['artist'].lower()
    artist = re.sub(" featuring.*", '', artist )
    artist = re.sub(" with .*", '', artist )
    artist = re.sub(" & .*", '', artist )
    artist = re.sub(" \/ .*", '', artist )
    artist = re.sub(" x .*", '', artist )
    artist = re.sub(" duet.*", '', artist )
    artist = re.sub("travi$", "travis", artist )
    artist = re.sub("jay z", "jay-z", artist )
    artist = re.sub("\\\"misdemeanor\\\"", "misdemeanor",  artist )
    artist = re.sub(" + .*", '', artist )
    artist = re.sub(" vs.*", '', artist )
    artist = artist.replace("'", "")
    artist = artist.replace("!", "")
    artist = artist.replace("?", "")
    artist = artist.replace("-", "")

    query = title + " " + artist
    print("Finding song!: ", query)
    try:
        results = sp.search(q=query)
    except:
        cache_token = token.get_access_token()
        sp = spotipy.Spotify(cache_token)
        results = sp.search(q=query)
    try:
        t = results['tracks']['items'][0]
    except:
        print("Could not find row", i)
        err.writerow([row['title'],row['artist'], artist, "COULD NOT FIND"])
        continue
    spotify_name = t['artists'][0]['name'].lower().replace("'", "").replace("!", "").replace("?", "").replace("-", "")
    if spotify_name!=artist and spotify_name[:spotify_name.find(" ")] not in artist  \
        and artist[:artist.find(" ")] not in spotify_name and levenshtein(spotify_name, artist) > 3:
        print("Song not found! Artist mismatch.")
        print("Song Name", row['title'])
        print("Artist Name", row['artist'])
        print("Row Number: ", i)
        print("Query: ", query)
        err.writerow([row['title'],row['artist'],artist, spotify_name])
        continue
    song['title'] = row['title']
    song['artist'] = row['artist'].encode("utf-8")
    song['album_name'] = t['album'].get('name').encode("utf-8")
    song['total_tracks'] = t['album'].get('total_tracks')
    song['release_date'] = t['album'].get('release_date')
    try:
        art_info = sp.search(q='artist:'+artist, type='artist')
    except:
        cache_token = token.get_access_token()
        sp = spotipy.Spotify(cache_token)
        art_info = sp.search(q='artist:'+artist, type='artist')
    try:
        song['genre'] = art_info['artists']['items'][0]['genres']
    except:
        song['genre'] = "NaN"
    try:
        song['artist_popularity'] = art_info['artists']['items'][0]['popularity']
    except:
        song['artist_popularity'] = "NaN"
    try:
        album = sp.album(t['album']['id'])
    except:
        cache_token = token.get_access_token()
        sp = spotipy.Spotify(cache_token)
        album = sp.album(t['album']['id'])
    song['album_popularity'] = album['popularity']
    song['label'] = album['label']
    song['is_explicit'] = t['explicit']
    song['song_popularity'] = t['popularity']
    try:
        features = sp.audio_features(t['id'])[0]
    except:
        cache_token = token.get_access_token()
        sp = spotipy.Spotify(cache_token)
        features = sp.audio_features(t['id'])[0]
    if features!=None:
        for feat, val in features.items():
            if feat not in ['track_href','analysis_url','uri','type','id']:
                key = "song_" + str(feat)
                song[key] = val
    else:
        for feat in ['song_popularity', 'song_danceability','song_energy','song_key',
        'song_loudness','song_mode','song_speechiness','song_acousticness',
        'song_instrumentalness','song_liveness','song_valence','song_tempo',
        'song_duration_ms','song_time_signature']:
            song[key] = "NaN"
    try:
        dw.writerow(song)
    except:
        print("Could not write for row", i)
        err.writerow([row['title'],row['artist'], artist, spotify_name])
        continue
    print("Done with Row : ", i)
output.close()
error.close()

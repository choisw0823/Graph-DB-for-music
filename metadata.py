import json
# from midiAnalyze import MIDI

path  = '~/'
scraped_genre = path+'MMD_scraped_genre.jsonl'
audio_matches = path+'MMD_audio_matches.tsv'
title_artist = path+'MMD_scraped_title_artist.jsonl'

title_artist_data = []

#title_artist
with open(title_artist, 'rt', encoding='UTF8') as f:
    for line in f:
        title_artist_data.append(json.loads(line))


for line in title_artist_data:
    print(line['md5'])


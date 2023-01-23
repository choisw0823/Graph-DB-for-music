from midiAnalyze import MIDI
from neptune import Neptune
from spotify import spotify
from metadata import metadata
import json

M = metadata()
i=0
sp = spotify()

for key, values in M.title_artist_data.items():
    if i==1:
        break
    i=1
    print(values)
    print(sp.get_id(name=values['title'], type='album'))
    print(sp.get_id(name=values['title'], type='track'))
    print(sp.get_id(name=values['artist'], type='artist'))

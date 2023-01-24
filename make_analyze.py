from midiAnalyze import MIDI
from neptune import Neptune
from spotify import spotify
from metadata import metadata
import json
import time

M = metadata()
sp = spotify()
l = len(M.title_artist_data)

for key, values in list(M.title_artist_data.items()):
    # track_info = None
    # album_info = None
    # audio_feature = None
    # artist_info = None
    # if i==10:
    #     break
    l-=1
    
    try:
        print('Left = ', l)
        result = sp.get_info(values)
        midi_result = {}
        if spotify is None:
            continue
        midi = MIDI(key)
        midi_result['instrument'] = midi.instrument()
        midi_result['key'] = midi.key()
        midi_result['chords'] = midi.extractChords()
        result['feature']['midi'] = midi_result
        time.sleep(0.5)
        
        with open("/home/ec2-user/Graph-DB-for-music/analyze_result.json", "a") as f:
            f.write(json.dumps(result))
        # track_dic = sp.get_id(name=values['title'], type='track')

        
        

        # artist_id = sp.get_id(name=values['artist'], type='artist')
        # print(track_dic, artist_id)
        # print(artist_id == track_dic['artist'])
        # if artist_id == track_dic['artist']:
        #     track_info = sp.get_track_info(track_dic['track'])
        #     album_info = sp.get_album_info(sp.get_id(name=values['title'], type='album'))
        #     audio_feature = sp.get_audio_features(track_dic['track'])
        #     artist_info = sp.get_artist_info(track_dic['artist'])
        #     print('track : ', track_info)    
        
    except Exception as e:
        print('Error occured during make_analyze.py : ', e)
        continue



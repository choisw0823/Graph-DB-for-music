from neptune import Neptune
import json 
import time 
import hashlib

N = Neptune()
contents=[]
genres = []
contents2=[]
contents3=[]
#{"track": {"id": "70V9otkdkxxiRjrdiHk6CO", "name": "Take a Letter, Maria", "popularity": 51, "release_date": "1969"}, 
# "artist": [{"id": "1BdNzKPyPDOhHdFhvwytQt", "name": "R.B. Greaves", "followers": 2115, "genre": [], "popularity": 35}], 
# "album": {"type": "album", "id": "58F2RoUSdk3GU6do32SuSE", "name": "R.B. Greaves", "popularity": 41, "release_date": "1969"}, 
# "feature": {"danceability": 0.582, "energy": 0.5, "loudness": -11.647, "valence": 0.971, "tempo": 160.414, 
# "midi": {"instrument": [null, "Trumpet", "Fretless Bass", "Alto Saxophone", "Baritone Saxophone", "Electric Guitar", "Trombone", "Tenor Saxophone"], "key": "F major",
#  "chords": ["iii43", "iii65", "v", "V64", "V53", "V", "-", "I64", "i43", "i7", "vii", "IV64", "V6", "iii42", "vi", "I6", "I53", "I"]}}}

# with open('/home/ec2-user/Dataset/MMD_scraped_genre.jsnol', 'r') as f:
#     for line in f:
#         l = json.loads(line)
#         genres.append(l)

with open('/home/ec2-user/Graph-DB-for-music/analyze_result.json', 'rt', encoding='UTF8') as f:
    for line in f:
        l = json.loads(line)
        contents.append(l)


with open('/home/ec2-user/Graph-DB-for-music/event_analyze_result.json', 'rt', encoding='UTF8') as f:
    for line in f:
        l = json.loads(line)
        contents2.append(l)

with open('/home/ec2-user/Graph-DB-for-music/get_related_artist_result.json', 'rt', encoding='UTF8') as f:
    for line in f:
        l = json.loads(line)
        contents3.append(l)

def vertex_analyze_result():
    print('Make Vertexes in analyze_result.json')
    i = 0
    for content in contents:
        try:
            N.create_node_if_not_exists('track', 'id', content['track']['id'], \
                {'id':content['track']['id'], 'name':content['track']['name'], 'release_date':content['track']['release_date'], 'popularity':content['track']['popularity'] })
    
            if content['artist'] is not None:
                for artist in content['artist']:
                    N.create_node_if_not_exists('artist', 'id', artist['id'], \
                        {'id':artist['id'], 'name':artist['name'], 'followers':artist['followers'], 'popularity':artist['popularity']})
                    if artist['genre'] is not None:
                        for genre in artist['genre']:
                            hash = hashlib.md5(genre.encode()).hexdigest()
                            N.create_node_if_not_exists('genre', 'id', hash, {'id':hash, 'name':genre})

            N.create_node_if_not_exists('album', 'id', content['album']['id'], \
                {'id':content['album']['id'], 'name':content['album']['name'], 'release_date':content['album']['release_date'], 'popularity':content['album']['popularity'] })    

            N.create_node_if_not_exists('audio_feature', 'id', content['track']['id'], \
                {'id':content['track']['id'], "danceability": content['feature']['danceability'], "energy": content['feature']['energy'], "loudness": content['feature']['loudness'], "valence": content['feature']['valence'], "tempo": content['feature']['tempo'] })
    
            if content['feature']['midi']['instrument'] is not None:
                for instrument in content['feature']['midi']['instrument']:
                    if instrument is not None:
                        hash = hashlib.md5(instrument.encode()).hexdigest()
                        N.create_node_if_not_exists('instrument', 'id', hash, {'id':hash, 'name':instrument})
            
            hash = hashlib.md5(content['feature']['midi']['key'].encode()).hexdigest()
            N.create_node_if_not_exists('key', 'id', hash, {'id':hash, 'key':content['feature']['midi']['key']})

            if content['feature']['midi']['chords'] is not None:
                for chord in content['feature']['midi']['chords']:
                    if chord != '-':
                        hash = hashlib.md5(chord.encode()).hexdigest()
                        N.create_node_if_not_exists('chord', 'id', hash, {'id':hash, 'chord':chord })
            i+=1
            print(str(i), 'th Line finished ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        except Exception as e:
            print('Error occured during making vertexes in analyze_result.json : ', e)
        
def edge_analyze_result():
    print('Make Edges in analyze_result.json')
    i = 0
    for content in contents:
        try:
            track_id = N.find_id('track', 'id', content['track']['id'])
            if track_id is None:
                continue
    
            if content['artist'] is not None:
                for artist in content['artist']:
                    artist_id = N.find_id('artist', 'id', artist['id'])
                    if artist_id is None:
                        continue
                    N.create_unique_edge(artist_id, 'artist_track', track_id, None )
                    
                    if artist['genre'] is not None:
                        for genre in artist['genre']:
                            hash = hashlib.md5(genre.encode()).hexdigest()
                            genre_id = N.find_id('genre', 'id', hash)
                            if genre_id is None:
                                continue
                            N.create_unique_edge(artist_id, 'artist_genre', genre_id, None)
                
                artist_id = N.find_id('artist', 'id', content['artist'][0]['id'])
                album_id = N.find_id('album', 'id', content['album']['id'])
                if artist_id is not None and album_id is not None:
                    N.create_unique_edge(artist_id, 'artist_album', album_id, None)
                if album_id is not None:
                    N.create_unique_edge(album_id, 'album_track', track_id, None)
                
            feature_id = N.find_id('audio_feature', 'id', content['track']['id'])
            if feature_id is not None:
                N.create_unique_edge(track_id, 'track_feature', feature_id, None)

            

            if content['feature']['midi']['instrument'] is not None:
                for instrument in content['feature']['midi']['instrument']:
                    if instrument is not None:
                        hash = hashlib.md5(instrument.encode()).hexdigest()
                        instrument_id = N.find_id('instrument', 'id', hash)
                        if instrument_id is None:
                            continue
                        N.create_unique_edge(track_id, 'track_instrument', instrument_id, None)

            hash = hashlib.md5(content['feature']['midi']['key'].encode()).hexdigest()
            key_id = N.find_id('key', 'id', hash)
            if key_id is not None:
                N.create_unique_edge(track_id, 'track_key', key_id, None)
            


            if content['feature']['midi']['chords'] is not None:
                for chord in content['feature']['midi']['chords']:
                    if chord != '-':
                        hash = hashlib.md5(chord.encode()).hexdigest()
                        chord_id = N.find_id('chord', 'id', hash)
                        N.create_unique_edge(track_id, 'track_chord', chord_id, None)
                        
            i+=1
            print(str(i), 'th Line finished ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        except Exception as e:
            print('Error occured during making edges in analyze_result.json : ', e)
#{"eventName": "Alice In Chains", "startDate": "2022-10-08T17:30:00-0400", "venueName": "Xfinity Center", "country": "US", "city": "Mansfield", "state": "MA", "longitude": -71.21065, "latitude": 41.99443, "address": "885 S. Main St.", "postalCode": "02048", "artistName": "Alice In Chains", "artistId": "64tNsm6TnZe2zpcMVMOoHL", "followers": 4331747, "genre": ["alternative metal", "alternative rock", "grunge", "hard rock", "nu metal", "rock"], "popularity": 72}

def vertex_event_analyze_result():
    print('Make Vertexes in event_analyze_result.json')
    i = 0
    for content in contents2:
        try:
            event_str = content['eventName']+content['startDate']+content['venueName']
            hash = hashlib.md5(event_str.encode()).hexdigest()

            if 'endDate' in content.keys():
                N.create_node_if_not_exists('event', 'id', hash, \
                    {'id':hash, 'name':content['eventName'], 'startDate':content['startDate'], 'endDate':content['endDate']})
            else:
                N.create_node_if_not_exists('event', 'id', hash, \
                    {'id':hash, 'name':content['eventName'], 'startDate':content['startDate']})

            
            N.create_node_if_not_exists('artist', 'id', content['artistId'], \
                {'id':content['artistId'], 'name':content['artistName'], 'followers':content['followers'], 'popularity':content['popularity']})

            if content['genre'] is not None:
                for genre in content['genre']:
                    hash = hashlib.md5(genre.encode()).hexdigest()
                    N.create_node_if_not_exists('genre', 'id', hash, {'id':hash, 'name':genre})

            
            venue_str = content['venueName']+content['country']
            hash = hashlib.md5(venue_str.encode()).hexdigest()

            venuedic = {'id':hash, 'name':content['venueName']}
            if 'longitude' in content.keys() and 'latitude' in content.keys():
                venuedic['longitude'] = content['longitude']
                venuedic['latitude'] = content['latitude']
            if 'address' in content.keys():
                venuedic['address'] = content['address']
            if 'postalCode' in content.keys():
                venuedic['postalCode'] = content['postalCode']
            
            N.create_node_if_not_exists('venue', 'id', hash, venuedic)

            hash = hashlib.md5(content['country'].encode()).hexdigest()
            N.create_node_if_not_exists('country', 'id', hash, \
                {'id':hash, 'name':content['country']})    

            hash = hashlib.md5(content['city'].encode()).hexdigest()
            N.create_node_if_not_exists('city', 'id', hash, \
                {'id':hash, 'name':content['city']})
            
            if 'state' in content.keys():
                hash = hashlib.md5(content['state'].encode()).hexdigest()
                N.create_node_if_not_exists('state', 'id', hash, \
                {'id':hash, 'name':content['state']})
    
            i+=1
            print(str(i), 'th Line finished ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        except Exception as e:
            print('Error occured during making vertexes in event_analyze_result.json : ', e)




def edge_event_analyze_result():
    print('Make edges in event_analyze_result.json')
    i = 0
    for content in contents2:
        try:
            event_str = content['eventName']+content['startDate']+content['venueName']
            hash = hashlib.md5(event_str.encode()).hexdigest()
            
            event_id = N.find_id('event', 'id', hash)
            artist_id = N.find_id('artist', 'id', content['artistId'])

            if event_id is not None and artist_id is not None:
                if 'endDate' in content.keys():
                    N.create_unique_edge(artist_id, 'artist_event', event_id, {'startDate':content['startDate'], 'endDate':content['endDate']})
                else:
                    N.create_unique_edge(artist_id, 'artist_event', event_id, {'startDate':content['startDate']})

            if content['genre'] is not None:
                for genre in content['genre']:
                    hash = hashlib.md5(genre.encode()).hexdigest()
                    genre_id = N.find_id('genre', 'id', hash)
                    if genre_id is None:
                        continue
                    N.create_unique_edge(artist_id, 'artist_genre', genre_id, None)

            
            venue_str = content['venueName']+content['country']
            hash = hashlib.md5(venue_str.encode()).hexdigest()

            venue_id = N.find_id('venue', 'id', hash)
            if venue_id is not None and event_id is not None:
                if 'endDate' in content.keys():
                    N.create_unique_edge(venue_id, 'venue_event', event_id, {'startDate':content['startDate'], 'endDate':content['endDate']})
                else:
                    N.create_unique_edge(venue_id, 'venue_event', event_id, {'startDate':content['startDate']})
            
            hash = hashlib.md5(content['country'].encode()).hexdigest()    
            country_id = N.find_id('country', 'id', hash)

            hash = hashlib.md5(content['city'].encode()).hexdigest()
            city_id = N.find_id('city', 'id', hash)

            state_id = None
            if 'state' in content.keys():
                hash = hashlib.md5(content['state'].encode()).hexdigest()
                state_id = N.find_id('state', 'id', hash)
                if city_id is not None and state_id is not None:
                    N.create_unique_edge(state_id, 'state_city', city_id, None)
                    N.create_unique_edge(city_id, 'city_venue', venue_id, None)
                if country_id is not None:
                    N.create_unique_edge(country_id, 'country_state', state_id, None)
            else:
                if city_id is not None and country_id is not None:
                    N.create_unique_edge(country_id, 'country_city', city_id, None)
                    N.create_unique_edge(city_id, 'city_venue', venue_id, None)
            

    
            i+=1
            print(str(i), 'th Line finished ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        except Exception as e:
            print('Error occured during making edges in event_analyze_result.json : ', e)

#{"mid": "3804CvHaDZ0SAOwvb84LpH", "id": "4Xfei8BCPubXEtzs6mCEin", "name": "Stone Dead", "genre": ["portuguese rock"], "popularity": 3, "followers": {"href": null, "total": 2193}}

def vertex_get_related_artist_result():
    print('Make Vertexes in get_related_artist_result.json')
    i = 0
    for content in contents3:
        try:
            N.create_node_if_not_exists('artist', 'id', content['id'], \
                {'id':content['id'], 'name':content['name'], 'followers':content['followers']['total'], 'popularity':content['popularity']})

            if content['genre'] is not None:
                for genre in content['genre']:
                    hash = hashlib.md5(genre.encode()).hexdigest()
                    N.create_node_if_not_exists('genre', 'id', hash, {'id':hash, 'name':genre})

            i+=1
            print(str(i), 'th Line finished ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        except Exception as e:
            print('Error occured during making vertexes in get_related_artist_result.json : ', e)




def edge_get_related_artist_result():
    print('Make edges in get_related_artist_result.json')
    i = 0
    for content in contents3:
        try:
            
            artist_id = N.find_id('artist', 'id', content['mid'])
            related_artist_id = N.find_id('artist', 'id', content['id'])

            if related_artist_id is None:
                continue

            # if content['genre'] is not None:
            #     for genre in content['genre']:
            #         hash = hashlib.md5(genre.encode()).hexdigest()
            #         genre_id = N.find_id('genre', 'id', hash)
            #         if genre_id is None:
            #             continue
            #         N.create_unique_edge(related_artist_id, 'artist_genre', genre_id, None)

            if artist_id is not None:
                #N.create_unique_edge(artist_id, 'related_artist', related_artist_id, None)
                N.create_unique_edge(related_artist_id, 'related_artist', artist_id, None)
            
            
            

    
            i+=1
            print(str(i), 'th Line finished ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        except Exception as e:
            print('Error occured during making edges in get_related_artist_result.json : ', e)




#edge_analyze_result()
#vertex_event_analyze_result()
#edge_event_analyze_result()
# with open('test.txt', 'w') as f:
#     for i in N.get_all_nodes():
#         f.write(json.dumps(i))

# with open('test2.txt', 'w') as f:
#     for i in N.get_all_edges():
#         f.write(json.dumps(i))

#print(N.get_connected_vertices(N.find_id('track', 'id', '1ethUluI5mc9zLDDTWyHg4'), 'track_key'))
#print(N.get_connected_vertices(N.find_id('venue', 'name', 'Kia Forum'), 'venue_event'))
#print(N.get_connected_vertices(N.find_id('artist', 'id', '1B8ySGDAiXTCvnJNH4HSCG'), 'artist_event'))
#print(N.get_connected_vertices_reverse(N.find_id('event', 'id', '15ae1b791f53b32effee368a64dfefb9'), 'venue_event'))
#print(N.get_connected_vertices(N.find_id('track', 'id', '4WUnM4KNZ0kjp0CUeoyOnS'), 'track_key'))
#print(N.get_connected_vertices(N.find_id('track', 'id', '4WUnM4KNZ0kjp0CUeoyOnS'), 'track_instrument'))
#print(N.get_connected_vertices_reverse(N.find_id('track', 'id', '4WUnM4KNZ0kjp0CUeoyOnS'), 'album_track'))
#print(N.get_connected_vertices(N.find_id('artist', 'id', '0lZoBs4Pzo7R89JM9lxwoT'), 'artist_genre'))
#print(N.get_connected_vertices_reverse(N.find_id('genre', 'name', 'new wave'), 'artist_genre'))
# with open('test.txt', 'w') as f:
#     for i in N.get_nodes_by_label('genre'):
#         f.write(json.dumps(i))


#print(N.get_nodes_by_label('genre'))
# genre_id = N.find_id('genre', 'name', 'new wave pop')
# print(genre_id)
# artist_id = N.find_id('artist', 'id', '3IhWQSrLj8EJjdvjFTpCyo')
# print(artist_id)

# N.create_node_if_not_exists('genre', 'id', 'test', {'id':'test'})
# N.create_node_if_not_exists('artist', 'id', 'test2', {'id':'test2'})
# genre_id = N.find_id('genre', 'id', 'test')
# artist_id = N.find_id('artist', 'id', 'test2')
# print('genreId ' , genre_id)
# print('artistId ', artist_id)

#print(N.get_connected_vertices(N.find_id('country', 'name', 'US'), 'country_state')[0]['name'][0])
# print(N.create_unique_edge(artist_id, 'artist_genre', genre_id, None))
#print(N.get_connected_vertices(artist_id, 'artist_album'))
#print(N.check_edge_exist(artist_id, 'artist_genre', genre_id))
#N.drop_all()
# N.drop_nodes_by_label('artist')
# print(len(N.get_all_nodes()))
# N.drop_nodes_by_label('venue')
# print(len(N.get_all_nodes()))
# N.drop_nodes_by_label('event')
# print(len(N.get_all_nodes()))
# N.drop_nodes_by_label('track')
# print(len(N.get_all_nodes()))
# N.drop_nodes_by_label('album')
# print(len(N.get_all_nodes()))
# N.drop_nodes_by_label('genre')
# print(len(N.get_all_nodes()))
# N.drop_nodes_by_label('audio_feature')
# print(len(N.get_all_nodes()))
# N.drop_nodes_by_label('chord')
# print(len(N.get_all_nodes()))
# N.drop_nodes_by_label('key')
# print(len(N.get_all_nodes()))
# N.drop_nodes_by_label('instrument')
# print(len(N.get_all_nodes()))
# N.drop_nodes_by_label('country')
# print(len(N.get_all_nodes()))
# N.drop_nodes_by_label('city')
# print(len(N.get_all_nodes()))
# N.drop_nodes_by_label('state')
# print(len(N.get_all_nodes()))

#print(N.get_all_edges())


#print(N.get_nodes_by_label('genre'))
# try:
#     with open('/home/ec2-user/Graph-DB-for-music/event_analyze_result.json', 'rt', encoding='UTF8') as f:
#         for line in f:
#             cache.add(line.strip())
# except Exception as e:
#     print('Error Occured during reading event_analyze_result.json : ', e)


# vertex_analyze_result()
# edge_analyze_result()
# vertex_event_analyze_result()
#edge_event_analyze_result()
# vertex_get_related_artist_result()
edge_get_related_artist_result()
# s = 'Altice Arena'+'Portugal'
# hash = hashlib.md5(s.encode()).hexdigest()  
# venue_id = N.find_id('venue', 'id', hash)
# print(N.get_node(venue_id))
# print(N.get_connected_vertices_reverse(venue_id, 'state_venue'))
#hash = hashlib.md5('Portugal'.encode()).hexdigest()
#country_id = N.find_id('country', 'id', hash)
#print(N.get_connected_vertices(country_id, 'country_city'))


# print(len(N.get_all_nodes()))
# print(len(N.get_nodes_by_label('artist')))
# print(len(N.get_nodes_by_label('album')))
# print(len(N.get_nodes_by_label('event')))
# print(len(N.get_nodes_by_label('track')))
# print(len(N.get_nodes_by_label('genre')))
# print(len(N.get_nodes_by_label('audio_feature')))
# print(len(N.get_nodes_by_label('chord')))
# print(len(N.get_nodes_by_label('key')))
# print(len(N.get_nodes_by_label('instrument')))
# print(len(N.get_nodes_by_label('country')))
# print(len(N.get_nodes_by_label('city')))
# print(len(N.get_nodes_by_label('state')))
# print(len(N.get_nodes_by_label('venue')))

from neptune import Neptune 
import hashlib

N = Neptune()
#{"track": {"id": "70V9otkdkxxiRjrdiHk6CO", "name": "Take a Letter, Maria", "popularity": 51, "release_date": "1969"}, 
# "album": {"type": "album", "id": "58F2RoUSdk3GU6do32SuSE", "name": "R.B. Greaves", "popularity": 41, "release_date": "1969"}, 
# "feature": {"danceability": 0.582, "energy": 0.5, "loudness": -11.647, "valence": 0.971, "tempo": 160.414, 
# "midi": {"instrument": [null, "Trumpet", "Fretless Bass", "Alto Saxophone", "Baritone Saxophone", "Electric Guitar", "Trombone", "Tenor Saxophone"], "key": "F major",
#  "chords": ["iii43", "iii65", "v", "V64", "V53", "V", "-", "I64", "i43", "i7", "vii", "IV64", "V6", "iii42", "vi", "I6", "I53", "I"]}}}

#{"eventName": "Alice In Chains", "startDate": "2019-08-13T19:00:00-0400", "venueName": "DTE Energy Music Theatre", 
# "country": "US", "city": "Clarkston", "state": "MI", "longitude": -83.38031, "latitude": 42.75101, "address": "7774 Sashabaw Rd", "postalCode": "48348", 
# "artistName": "Underoath", "artistId": "3GzWhE2xadJiW8MqRKIVSK", "followers": 555334, "genre": ["christian metal", "christian metalcore", "
# melodic metalcore", "metalcore", "pop punk", "post-hardcore", "screamo", "tampa indie"], "popularity": 58}

inp = {'artistName' : None,'artistId':None, 'popularity':None, 'followers':None, 'genre':None, 
'track':{'name':None, 'id':None, 'popularity':None, 'audio_feature':{"danceability": None, "energy": None, "loudness": None, "valence": None, "tempo": None, \
    'instrument':None, 'key':None, 'chords':None}, }, \
    'album':{'id': None,'popularity':None, 'name':None}, \
    'eventName':None, 'startDate':None, 'endDate':None,  'venueName':None, 'country':None, 'city':None, 'state':None, 'longitude':None, 'latitude':None, 'address':None, 'postalCode':None,\
    'country':None, 'state':None, 'city':None}

inp['country'] = 'US'
inp['artistId'] = '64tNsm6TnZe2zpcMVMOoHL'
inp['genre'] = ['alternative metal']
inp['popularity'] = 72

#print(N.g.V().hasLabel('country').has('name', inp['country']).out().as_('states').out().as_('cities').out().as_('venues').outE('venue_event').as_('edge').inV().values('name').toList())
#.hasLabel('artist').back('edge').outV().back('cities').back('states').back('venues').values('name').toList()
print('yees')
venue_list = set()
#N.g.V().hasLabel('country').has('name', inp['country']).union(N.__.out('country_state').has('name', ), N.__.out('located_in').out('located_in').has('name', '{city_name}')).out('located_in').hasLabel('venue').values('name').toList()
#g.V().hasLabel('country').has('name', '{country_name}').out('located_in').repeat(out('located_in')).until(hasLabel('venue')).hasLabel('venue').values('name').toList()

if inp['city'] is not None:
    hash = hashlib.md5(inp['city'].encode()).hexdigest()
    city_id = N.find_id('city', 'id', hash)
    if city_id:
        for i in N.get_connected_vertices(city_id, 'city_venue'):
            venue_list.add(i['name'][0])

elif inp['state'] is not None:
    hash = hashlib.md5(inp['state'].encode()).hexdigest()
    state_id = N.find_id('state', 'id', hash)
    if state_id:
        city_list = N.get_connected_vertices(state_id, 'state_city')
        for city in city_list:
            city_id = N.find_id('city', 'id', city['id'][0])
            if city_id:
                for i in N.get_connected_vertices(city_id, 'city_venue'):
                    venue_list.add(i['name'][0])
    
elif inp['country'] is not None:
    hash = hashlib.md5(inp['country'].encode()).hexdigest()
    country_id = N.find_id('country', 'id', hash)
    if country_id:
        state_list = N.get_connected_vertices(country_id, 'country_state')      
        for state in state_list:
            state_id = N.find_id('state', 'id', state['id'][0])
            if state_id:
                city_list = N.get_connected_vertices(state_id, 'state_city')
                for city in city_list:
                    city_id = N.find_id('city', 'id', city['id'][0])
                    if city_id:
                        for i in N.get_connected_vertices(city_id, 'city_venue'):
                            venue_list.add(i['name'][0])
        
        city_list = N.get_connected_vertices(country_id, 'country_city')
        #print(city_list)
        for city in city_list:
                    city_id = N.find_id('city', 'id', city['id'][0])
                    if city_id:
                        for i in N.get_connected_vertices(city_id, 'city_venue'):
                            #print(i)
                            venue_list.add(i['name'][0])

print('Prediction By Location Finished')
#print(venue_list)
#repeat until 
related_artist = []
if inp['artistId'] is not None:
    r = N.get_connected_vertices(N.find_id('artist', 'id', inp['artistId']), 'related_artist')
    if r is not None:
        for i in r:
            if inp['popularity'] is not None:
                if i['popularity'][0] // 10 == inp['popularity'] // 10: 
                    related_artist.append(i['id'][0])
            else:
                related_artist.append(i['id'][0])  
            
    r = N.get_connected_vertices_reverse(N.find_id('artist', 'id', inp['artistId']), 'related_artist')
    if r is not None:
        for i in r:
            if inp['popularity'] is not None:
                if i['popularity'][0] // 10 == inp['popularity'] // 10: 
                    related_artist.append(i['id'][0])
            else:
                related_artist.append(i['id'][0])  
            
    related_artist.append(inp['artistId'])

elif inp['artistName'] is not None:
    artist_id = N.find_id('artist', 'name', inp['artistName'])
    if artist_id:
        r = N.get_connected_vertices(artist_id, 'related_artist')
        if r is not None:
            for i in r:
                related_artist.append(i['id'][0])
        r = N.get_connected_vertices_reverse(artist_id, 'related_artist')
        if r is not None:
            for i in r:
                related_artist.append(i['id'][0])
    related_artist.append(artist_id)
#print(related_artist)
#print(N.get_connected_vertices_reverse(N.find_id('artist', 'id', inp['artistId']), 'related_artist'))
#print(N.get_connected_vertices_reverse(N.find_id('artist', 'id', related_artist[0]['id'][0]), 'related_artist'))
temp = set()
while(len(related_artist) != 0):
    artist = related_artist[0]
    r = N.get_connected_vertices_reverse(N.find_id('artist', 'id', artist), 'related_artist')
    for i in r:
        if i['id'][0] not in temp:
            if i['id'][0] not in related_artist:
                if inp['popularity'] is not None:
                    if i['popularity'][0] // 10 == inp['popularity'] // 10: 
                        related_artist.append(i['id'][0])
                else:
                    related_artist.append(i['id'][0])  
    r = N.get_connected_vertices(N.find_id('artist', 'id', artist), 'related_artist')
    for i in r:
        if i['id'][0] not in temp:
            if inp['popularity'] is not None:
                if i['popularity'][0] // 10 == inp['popularity'] // 10: 
                    related_artist.append(i['id'][0])
                else:
                    related_artist.append(i['id'][0])  
    
    temp.add(artist)
    related_artist.remove(artist)
    
related_artist = list(temp) 
print('Related Artist Search Finished')
#print(related_artist)
temp_venue = set()

for artist in related_artist:
    artist_id = N.find_id('artist', 'id', artist)
    e = N.get_connected_vertices(artist_id, 'artist_event')
    for i in e:
        event_id = N.find_id('event', 'id', i['id'][0])
        v = N.get_connected_vertices_reverse(event_id, 'venue_event')
        for j in v:
            temp_venue.add(j['name'][0])

print('Venue Search By Related Artist Finished')
#print(temp_venue)
venue_list = venue_list & temp_venue


genre_artist = set()
if inp['genre'] is not None:
    for genre in inp['genre']:
        genre_id = N.find_id('genre', 'name', genre)
        if genre_id:
            for i in N.get_connected_vertices_reverse(genre_id, 'artist_genre'):
                if inp['popularity'] is not None:
                    if i['popularity'][0] // 10 == inp['popularity'] // 10: 
                        genre_artist.add(i['id'][0])
                else:
                    genre_artist.add(i['id'][0])  
    temp_venue = set()

    for artist in genre_artist:
        artist_id = N.find_id('artist', 'id', artist)
        e = N.get_connected_vertices(artist_id, 'artist_event')
        for i in e:
            event_id = N.find_id('event', 'id', i['id'][0])
            v = N.get_connected_vertices_reverse(event_id, 'venue_event')
            for j in v:
                temp_venue.add(j['name'][0])
    venue_list = venue_list & temp_venue

print('Venue Search By Genre Finished')

print(venue_list)


# iam key ?????? ?????? ????????? ??????????????? //
#  predict??? ??? ?????? gremlin?????? ???????????? ?????? ?????? // 
# ?????????????????? ???????????????, ???????????? ???????????? ?????? gremlin?????? ?????????. 
# ????????? ?????? ??????, ??????????????? ?????? ????????? ????????? venue??? ????????? ?????????. 
# ?????? ???????????? ????????? ?????? ??? ????????? ??????????????? ????????? ?????????????????? ????????? ????????? ????????? ??????

# 2??? 10??? 3???
# ????????? ????????? ??? ????????? ?????? ??????
# city->venue ??????
# ????????? ????????? ?????????
# ????????? ?????? ??????
# ????????? 1?????? ????????? ?????????
# ??????????????? ????????? ppt
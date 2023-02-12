import neptune
import hashlib

N = neptune.Neptune()

inp = {'artistName' : None,'artistId':None, 'popularity':None, 'followers':None, 'genre':None, 
'track':{'name':None, 'id':None, 'popularity':None},
'audio_feature':{"danceability": None, "energy": None, "loudness": None, "valence": None, "tempo": None, \
    'instrument':None, 'key':None, 'chords':None}, \
    'album':{'id': None,'popularity':None, 'name':None}, \
    'eventName':None, 'startDate':None, 'endDate':None,  'venueName':None, 'country':None, 'city':None, 'state':None, 'longitude':None, 'latitude':None, 'address':None, 'postalCode':None,\
    'country':None, 'state':None, 'city':None}

inp['country'] = 'Portugal'
inp['state']= 'MN'
inp['artistId'] = '7oZLKL1GjYiaAgssXsLmW8'
inp['genre'] = ['alternative metal']
inp['popularity'] = 72

venue_set = set()
result = None
#Search For Location
if inp['city'] is not None:
    result = N.g.V().hasLabel('city').has('name', inp['city']).outE('city_venue').inV().values('id').toList()
elif inp['state'] is not None:
    result = N.g.V().hasLabel('state').has('name', inp['state']).outE('state_city').inV().outE('city_venue').inV().values('id').toList()

elif inp['country'] is not None:
    result = N.g.V().hasLabel('country').has('name', inp['country']).outE('country_state').inV().outE('state_city').inV().outE('city_venue').inV().values('id').toList()
    if len(result) == 0:
        result = N.g.V().hasLabel('country').has('name', inp['country']).out().as_('cities').out().values('id').toList()
if result is not None:
    venue_set = set(result)

#Search For Related Artist
result = None
artistId = None
if inp['artistName'] is not None:
    artistId = N.find_id('artist', 'name', inp['artistName'])
if inp['artistId'] is not None:
    artistId = inp['artistId']
    
if artistId is not None:
    result = N.g.V().hasLabel('artist').has('id', artistId).repeat(neptune.__.out('related_artist')).emit().dedup().out('artist_event').inE('venue_event').outV().dedup().values('id').toList()
#print(result)
if result is not None and len(venue_set) != 0:
    venue_set = set(result) & venue_set
elif result is not None:
    venue_set = result


result = None
if inp['genre'] is not None:
    for genre in inp['genre']:
        if result is None:
            result = set(N.g.V().hasLabel('genre').has('name', genre).inE('artist_genre').outV().out('artist_event').inE('venue_event').outV().dedup().values('id').toList())
        else:
            result = result & set(N.g.V().hasLabel('genre').has('name', genre).inE('artist_genre').outV().out('artist_event').inE('venue_event').outV().dedup().values('id').toList())
            
if result is not None and len(venue_set) != 0:
    venue_set = set(result) & venue_set
elif result is not None:
    venue_set = result


if inp['trackName'] is not None:
    trackId = N.find_id('track', 'name', inp['trackName'])
if inp['trackId'] is not None:
    trackId = inp['trackId']



#print(len(venue_set))


# a = N.create_node_if_not_exists('artist', 'id', 'test', {'id': 'test'})
# b = N.create_node_if_not_exists('artist', 'id', 'test2', {'id': 'test2'})
# print(a,b)
# N.create_unique_edge(a, 'related_artist', b, None)
#print(N.find_id('artist', 'id', '3TQ7yQyNz2JvOXqiO5Tpz2'))
#print(N.get_connected_vertices(N.find_id('artist', 'id', '3TQ7yQyNz2JvOXqiO5Tpz2'), 'related_artist'))
# a = N.find_id('artist', 'id', 'test')
# b = N.find_id('artist', 'id', 'test2')
# c = N.create_node_if_not_exists('artist', 'id', 'test4', {'id': 'test4'})
# N.create_unique_edge(b, 'related_artist', c, None)
# d = N.create_node_if_not_exists('artist', 'id', 'test5', {'id': 'test5'})
# N.create_unique_edge(c, 'related_artist', d, None)
#print(a,b)
#print(N.get_connected_vertices(a, 'related_artist'))
#result = N.g.V().hasLabel('country').has('name', inp['country']).out().as_('states').out().as_('cities').out().as_('venues').outE('venue_event').as_('edge').inV().values('id').toList()
#.hasLabel('artist').back('edge').outV().back('cities').back('states').back('venues').values('name').toList()
#N.g.V().hasLabel('country').has('name', inp['country']).union(N.__.out('country_state').has('name', inp['state'] ), N.__.out('country_state').out('state_city').has('name', inp['city'])).out('city_venue').hasLabel('venue').values('name').toList()
#N.g.V().hasLabel('country').has('name', '{country_name}').out('located_in').repeat(out('located_in')).until(hasLabel('venue')).hasLabel('venue').values('name').toList()

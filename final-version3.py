import neptune
import hashlib
import numpy as np
import json 
import time
import datetime


#for audio_feature
def cosine_similarity(a, b, threshold):
    compare = [a['tempo'][0], a['danceability'][0], a['loudness'][0], a['valence'][0], a['energy'][0]]
    dot_product = np.dot(compare, b)
    magnitude_a = np.sqrt(np.dot(compare, compare))
    magnitude_b = np.sqrt(np.dot(b, b))

    if dot_product / (magnitude_a * magnitude_b) > threshold:
        return True
    else:
        return False

#for instrument
def jaccard_similarity(set1, set2):
    s = len(set1 & set2) / len(set1 | set2)
    return s

#for chord
def jaccard_similarity_chord(set1, set2):
    #print(set1, set2)
    p1 = set()
    p2 = set()
    for i in set1:
        i = i.replace('4', '')
        i = i.replace('3', '')
        i = i.replace('5', '')
        p1.add(i)

    for i in set2:
        i = i.replace('4', '')
        i = i.replace('3', '')
        i = i.replace('5', '')
        p2.add(i)

    s = len(p1 & p2) / len(p1 | p2)

    return s
#for instrument
def get_similarity(track1, track2, mapping):
    set1 = set()
    set2 = set()
    flag = 0
    split = ['.', ',', '/', '(', ')', '-', "'", '"', '-', '_', '#', '+','\\','1','2','3','4','5','6','7','8','9','0','<', '>', '{', '}', '=', '*', '=' ]

    for instrument in track1:
        for s in split:
            r = instrument.lower()
            r = r.replace(s, ' ')
        li = r.split()
        for l in li:
            for t in split:
                l = l.replace(t, ' ')
            for i in l.split():
                if i in mapping.keys():
                    set1.add(mapping[i])
                    flag = 1
        # if flag==0:
        #     set1.add(instrument)
        # flag = 0

    for instrument in track2:
        for s in split:
            r = instrument.lower()
            r = r.replace(s, ' ')
        li = r.split()
        for l in li:
            for t in split:
                l = l.replace(t, ' ')
            for i in l.split():
                if i in mapping.keys():
                    set2.add(mapping[i])
                    flag = 1
        # if flag==0:
        #     set2.add(instrument)
        # flag = 0
    return jaccard_similarity(set1, set2)

    

N = neptune.Neptune()
#print(N.g.V().hasLabel('instrument').has('name', 'Organ Leslie').in_('track_instrument').toList())


inp = {'artistName' : None,'artistId':None, 'popularity':None, 'followers':None, 'genre':None, 
'track':{'name':None, 'id':None, 'popularity':None},
'audio_feature':{"danceability": None, "energy": None, "loudness": None, "valence": None, "tempo": None, \
    'instrument':None, 'key':None, 'chords':None}, \
    'album':{'id': None,'popularity':None, 'name':None}, \
    'eventName':None, 'startDate':None, 'endDate':None,  'venueName':None, 'country':None, 'city':None, 'state':None, 'longitude':None, 'latitude':None, 'address':None, 'postalCode':None,\
    'country':None, 'state':None, 'city':None}

inp['country'] = 'UK'
#inp['state']= 'MN'
inp['artistId'] = '4tiFScdzVOm0kGSq4d0l2K'
inp['genre'] = ["early music", "english renaissance", "renaissance"]
#inp['popularity'] = 72
inp['track']['id'] = '5SuRjWCCaRYJwUI9TDHCUe'
#inp['audio_feature']['instrument'] =  ["Drums (Standard Kit)", "Electric Bass", "Overdrive Guitar", "Bass Guitar", "Ava Adore", "Clean Guitar", "Optimised for XG", "Electric Guitar", "Midi File by Sayed Hoda", "Bass Drum (Rock Kit)", "=========================", "Song by Billy Corgan/ Smashing Pumpkins", "AHODA@compuserve.com"]
#inp['audio_feature']['chords'] = ['V64', 'I53', 'ii', 'v', 'I64', 'i', 'III53', 'iii43', 'V53', 'i53', 'iv7', 'III6', 'V', 'VII53']
venue_set = set()
result = None


#Search For Location
start = time.time()
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
end = time.time()
print('Search For Location Finished : ', datetime.timedelta(seconds=end-start) )


#Search For Related Artist
start = time.time()
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
end = time.time()
print('Search For Related Artist Finished : ', datetime.timedelta(seconds=end-start) )


#Search For Genre
start = time.time()
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
end = time.time()

print('Search For Genre Finished : ', datetime.timedelta(seconds=end-start))


#Search for Track
# trackId = None
# result=None
# if inp['track']['name'] is not None:
#     trackId = N.find_id('track', 'name', inp['track']['name'])
# if inp['track']['id'] is not None:
#     trackId = inp['track']['id']
# if trackId is not None:
#     threshold = 0.8
#     audio_feature = N.g.V().hasLabel('audio_feature').has('id', trackId).valueMap().next()
#     audio_feature = [audio_feature['tempo'][0], audio_feature['danceability'][0], audio_feature['loudness'][0], audio_feature['valence'][0], audio_feature['energy'][0]]
#     #print(audio_feature)
#     #result = set(map(lambda a: cosine_similarity(a, audio_feature, threshold)['id'][0] if cosine_similarity(a, audio_feature, threshold) is not False else None, N.g.V().hasLabel('audio_feature').valueMap()))
    
#     for feature in N.g.V().hasLabel('audio_feature').valueMap().toList():
#         s = cosine_similarity(feature, audio_feature, threshold)
#         if s:
#             s = s['id'][0]
#             inst = N.g.V().hasLabel('track').has('id', s).out('track_instrument').values('name').toList()
#             with open('/home/ec2-user/Graph-DB-for-music/instrument', 'rt', encoding='UTF8') as f:
#                 mapping = json.loads(f.readline())
            

#             #instrument
#             if get_similarity(N.g.V().hasLabel('track').has('id', trackId).out('track_instrument').values('name').toList(), inst, mapping) > 0.4:
#                 #chords
#                 chords = N.g.V().hasLabel('track').has('id', s).out('track_chord').values('chord').toList()
#                 if jaccard_similarity(set(N.g.V().hasLabel('track').has('id', trackId).out('track_chord').values('chord').toList()), set(chords)) > 0.4:
#                     print(s)
#                     if result is None:
#                         result = set(N.g.V().hasLabel('track').has('id', s).inE('artist_track').outV().out('artist_event').inE('venue_event').outV().dedup().values('id').toList())
#                     else:
#                         result = result & set(N.g.V().hasLabel('track').has('id', s).inE('artist_track').outV().out('artist_event').inE('venue_event').outV().dedup().values('id').toList())
            

# if result is not None and len(venue_set) != 0:
#     venue_set = set(result) & venue_set
# elif result is not None:
#     venue_set = result

trackId = None
result=None
threshold = 0.8
if inp['track']['name'] is not None:
    trackId = N.find_id('track', 'name', inp['track']['name'])
if inp['track']['id'] is not None:
    trackId = inp['track']['id']
if trackId is not None:
    
    #audio_feature = N.g.V().hasLabel('audio_feature').has('id', trackId).valueMap().next()
    #audio_feature = [audio_feature['tempo'][0], audio_feature['danceability'][0], audio_feature['loudness'][0], audio_feature['valence'][0], audio_feature['energy'][0]]
    inst = N.g.V().hasLabel('track').has('id', trackId).out('track_instrument').values('name').toList()
    chords = N.g.V().hasLabel('track').has('id', trackId).out('track_chord').values('chord').toList()
    # inp['audio_feature']['tempo'] = audio_feature[0]
    # inp['audio_feature']['danceability'] = audio_feature[1]
    # inp['audio_feature']['loudness'] = audio_feature[2]
    # inp['audio_feature']['valence'] = audio_feature[3]
    # inp['audio_feature']['energy'] = audio_feature[4]
    inp['audio_feature']['instrument'] = inst
    inp['audio_feature']['chords'] = chords


#print(inp['audio_feature'])
#print('Search For Track Finished')

#print(N.g.V().hasLabel('audio_feature').valueMap().filter_(lambda vertex, audio_feature=audio_feature: cosine_similarity(vertex, audio_feature, 0.6)))
#print(N.g.V().hasLabel('audio_feature').map(lambda vertex : cosine_similarity(vertex, audio_feature, threshold) != False).valueMap().toList())
#print(N.g.V().hasLabel('audio_feature').filter_(neptune.__.valueMap().map(lambda vertex: cosine_similarity(vertex, audio_feature) > 0.6)))
#N.g.V().hasLabel("audio_feature").where(neptune.__.filter_(lambda: "lambda x: ‘abc' in x.get().value('name').lower()")).values("name").toList()
# audio_feature = [inp['audio_feature']['tempo'] , inp['audio_feature']['danceability'] ,inp['audio_feature']['loudness'] , inp['audio_feature']['valence'] , inp['audio_feature']['energy']]
# start = time.time()
# li = (list(map(lambda vertex : N.g.V().hasLabel('track').has('id', vertex['id'][0]).in_('artist_track').out('artist_event').in_('venue_event').dedup().values('id').toList() if cosine_similarity(vertex, audio_feature, 0.6)==True else None, N.g.V().hasLabel('audio_feature').valueMap())))
# end = time.time()
# print('By query : ', datetime.timedelta(seconds=end-start))
# print(len(li))
# with open('tttt', 'wt') as f:
#     f.write(json.dumps(li))
# exit()


# result1 = None
# result2 = None
# result3 = None
# with open('/home/ec2-user/Graph-DB-for-music/instrument', 'rt', encoding='UTF8') as f:
#             mapping = json.loads(f.readline())
# start = time.time()
# for track in N.g.V().hasLabel('track').toList():
#     if inp['audio_feature']['tempo'] is not None and  inp['audio_feature']['danceability'] is not None and \
#         inp['audio_feature']['loudness'] is not None and inp['audio_feature']['valence'] is not None and  inp['audio_feature']['energy'] is not None:

#             audio_feature = [inp['audio_feature']['tempo'] , inp['audio_feature']['danceability'] ,inp['audio_feature']['loudness'] , inp['audio_feature']['valence'] , inp['audio_feature']['energy']]
#             if cosine_similarity(N.g.V(track).out('track_feature').valueMap().next(), audio_feature, 0.7):
#                 if result1 is None:
#                     result1 = set(N.g.V(track).in_('artist_track').out('artist_event').in_('venue_event').dedup().values('id').toList())
#                 else:
#                     result1 = result1 | set(N.g.V(track).in_('artist_track').out('artist_event').in_('venue_event').dedup().values('id').toList())

            
#     if inp['audio_feature']['instrument'] is not None:
#         if get_similarity(N.g.V(track).out('track_instrument').values('name').toList(), inp['audio_feature']['instrument'], mapping) > 0.6:
#             if result2 is None:
#                 result2 = set(N.g.V(track).in_('artist_track').out('artist_event').in_('venue_event').dedup().values('id').toList())
#             else:
#                 result2 = result2 | set(N.g.V(track).in_('artist_track').out('artist_event').in_('venue_event').dedup().values('id').toList())
#     if inp['audio_feature']['chords'] is not None:
#         if jaccard_similarity_chord(set(N.g.V(track).out('track_chord').values('chord').toList()), set(inp['audio_feature']['chords'])) > 0.6:
#             if result3 is None:
#                 result3 = set(N.g.V(track).in_('artist_track').out('artist_event').in_('venue_event').dedup().values('id').toList())
#             else:
#                 result3 = result3  | set(N.g.V(track).in_('artist_track').out('artist_event').in_('venue_event').dedup().values('id').toList())
# end = time.time()
# print('Search For track Finished : ', datetime.timedelta(seconds=end-start))

# for r in [result1, result2, result3]:
#     if r is not None:
#         if len(venue_set) == 0:
#             venue_set = r
#         else:
#             venue_set = venue_set & r

#Search For Audio_feature
start = time.time()
result=None
threshold = 0.7
if inp['audio_feature']['tempo'] is not None and  inp['audio_feature']['danceability'] is not None and \
    inp['audio_feature']['loudness'] is not None and inp['audio_feature']['valence'] is not None and  inp['audio_feature']['energy'] is not None:
    audio_feature = [inp['audio_feature']['tempo'] , inp['audio_feature']['danceability'] ,inp['audio_feature']['loudness'] , inp['audio_feature']['valence'] , inp['audio_feature']['energy']]
    res = N.g.V().hasLabel('audio_feature').valueMap().toList()
    

    for feature in res:
        s = cosine_similarity(feature, audio_feature, threshold)
        if s:
            s = feature['id'][0]
            if result is None:
                result = set(N.g.V().hasLabel('track').has('id', s).in_('artist_track').out('artist_event').in_('venue_event').dedup().values('id').toList())
            else:
                result = result | set(N.g.V().hasLabel('track').has('id', s).in_('artist_track').out('artist_event').in_('venue_event').dedup().values('id').toList())
#print(len(result)) 
elif trackId is not None:
    #N.g.V().hasLabel('audio_feature').has('id', trackId).outE('similarity').as_('edge').where('edge'.property('value') > 0.7).inV().valueMap().toList()
    result = set(N.g.V().hasLabel('audio_feature').has('id', trackId).outE('similarity').has('value', neptune.P.gt(threshold)).inV().in_('track_feature').in_('artist_track').out('artist_event').in_('venue_event').dedup().values('id').toList())
if result is not None and len(venue_set) != 0:
    venue_set = set(result) & venue_set
elif result is not None:
    venue_set = result

end = time.time()
print('Search For audio feature Finished : ', datetime.timedelta(seconds=end-start))
#print(venue_set)

#Search for Instrument
start = time.time()
result=None
threshold = 0.6
if inp['audio_feature']['instrument'] is not None: #and inp['track']['name'] is None and inp['track']['id'] is None:
    with open('/home/ec2-user/Graph-DB-for-music/instrument', 'rt', encoding='UTF8') as f:
        mapping = json.loads(f.readline())
    #print(N.g.V().hasLabel('track').map(lambda : "x->x.values('id')").next())
    for track in N.g.V().hasLabel('track').toList():
        

        if get_similarity(N.g.V(track).out('track_instrument').values('name').toList(), inp['audio_feature']['instrument'], mapping) > threshold:
            if result is None:
                result = set(N.g.V(track).in_('artist_track').out('artist_event').in_('venue_event').dedup().values('id').toList())
            else:
                result = result | set(N.g.V(track).in_('artist_track').out('artist_event').in_('venue_event').dedup().values('id').toList())
    
if result is not None and len(venue_set) != 0:
    venue_set = set(result) & venue_set
elif result is not None:
    venue_set = result  

end = time.time()
print('Search For instrument Finished : ', datetime.timedelta(seconds=end-start))
#print(venue_set)
# time.sleep(3)

#Search For Chords
start = time.time()
result=None
threshold = 0.6
if inp['audio_feature']['chords'] is not None: #and inp['track']['name'] is None and inp['track']['id'] is None:
    #print(inp['audio_feature']['chords'])
    for track in N.g.V().hasLabel('track').values('id').toList():
        if jaccard_similarity_chord(set(N.g.V().hasLabel('track').has('id', track).out('track_chord').values('chord').toList()), set(inp['audio_feature']['chords'])) > threshold:
            if result is None:
                result = set(N.g.V().hasLabel('track').has('id', track).in_('artist_track').out('artist_event').in_('venue_event').dedup().values('id').toList())
            else:
                result = result  | set(N.g.V().hasLabel('track').has('id', track).in_('artist_track').out('artist_event').in_('venue_event').dedup().values('id').toList())
if result is not None and len(venue_set) != 0:
    venue_set = set(result) & venue_set
elif result is not None:
    venue_set = result 

end = time.time()

print('Search For chords Finished : ', datetime.timedelta(seconds=end-start))

v = []
#print(venue_set)
for venue in venue_set:
    v.append(N.g.V().hasLabel('venue').has('id', venue).values('name').next())
print(v)


#Prediction For Time
start = time.time()



    # p = N.g.V().hasLabel("audio_feature").map(lambda vertex: vertex)
    # print(p)
    # r = p.flatMap(lambda a: cosine_similarity(a, audio_feature, threshold)).filter_(lambda sim: sim > threshold)
    # print(r)
    #similar_vertices = N.g.V().hasLabel('audio_feature').filter_(lambda vertex: cosine_similarity(vertex, audio_feature) > threshold).valueMap().toList()

#print(similar_vertices)
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

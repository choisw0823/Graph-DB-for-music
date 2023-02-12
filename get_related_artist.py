from spotify import spotify
import json 
import time 

contents = []
cache = set()
sp = spotify()

with open("/home/ec2-user/Graph-DB-for-music/event_analyze_result.json", "r") as f:
     for line in f:
        l = json.loads(line)
        contents.append(l)

try:
    with open("/home/ec2-user/Graph-DB-for-music/get_related_artist_result.json", "r") as f:
        for line in f:
            l = json.loads(line)
            cache.add(l['mid'])
except Exception as e:
    print('No file exist : ', e)


line = 0
try:    
    for content in contents:
        line += 1
        if content['artistId'] in cache:
            print('Related Artist Passed : ', content['artistName'], 'line : ', str(line),  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            continue 

        artists = sp.get_related_artist(content['artistId'])
        
        for artist in artists['artists']:
            with open("/home/ec2-user/Graph-DB-for-music/get_related_artist_result.json", "a") as f:
                result = {'mid': content['artistId'],  'id':artist['id'], 'name':artist['name'], 'genre':artist['genres'], 'popularity':artist['popularity'], 'followers':artist['followers']}
                f.write(json.dumps(result, default=str))
                f.write('\n')
        cache.add(content['artistId'])
        print('Related Artist Finished : ', content['artistName'], 'line : ', str(line),  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        time.sleep(2)
except Exception as e:
    print('Error Occured during get_related_artist.py : ', e)


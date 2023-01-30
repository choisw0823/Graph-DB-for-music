from songkick import SongKickScraper
from spotify import spotify 
import json 
import time 


sp = spotify()
ss = SongKickScraper()


contents = []
cache = set()


with open('/home/ec2-user/Graph-DB-for-music/analyze_result.json', 'rt', encoding='UTF8') as f:
    for line in f:
        l = json.loads(line)
        contents.append(l)
try:
    with open('/home/ec2-user/Graph-DB-for-music/event_analyze_result.json', 'rt', encoding='UTF8') as f:
        for line in f:
            cache.add(line.strip())
except Exception as e:
    print('Error Occured during reading event_analyze_result.json : ', e)

length = len(cache)
cnt = 0
flag = 0
for content in contents:
    if content['artist'][0]['name'] == 'Allman Brothers Band':
        flag = 1
    if flag==0:
        print('Passed : ', content['artist'][0]['name'])
        continue
    
    try:
        page = 1
        total_page=1
        events = []
        for artist_info in content['artist']:

                while(page <= total_page):
                    try:
                        res = ss.get_artist_events_json(artist_info['name'], page)
                        if res is not None:
                            events, total_page = res 
                        #print(events)
                        for event in events:

                            #print(event)
                            if (event['location']['@type'] != 'Place'):
                                continue
                            result = {'eventName' : event['name'], 'startDate':event['startDate'], 'venueName':event['location']['name'], 'country':event['location']['address']['addressCountry'],\
                                 'city':event['location']['address']['addressLocality'] }
                        
                            if 'addressRegion' in event['location']['address'].keys():
                                result['state'] = event['location']['address']['addressRegion']
                            if 'geo' in event['location'].keys():
                                result['longitude'] = event['location']['geo']['longitude']
                                result['latitude'] = event['location']['geo']['latitude']
                            if 'streetAddress' in event['location']['address'].keys():
                                result['address'] = event['location']['address']['streetAddress']
                            if 'postalCode' in event['location']['address'].keys():
                                result['postalCode'] = event['location']['address']['postalCode']

                            for artist in event['performer']:
                                if artist['name'] == artist_info['name']:
                                    result['artistName'] = artist_info['name']
                                    result['artistId'] = artist_info['id']
                                    result['followers'] = artist_info['followers']
                                    result['genre'] = artist_info['genre']
                                    result['popularity'] = artist_info['popularity']
                                    if json.dumps(result, default=str) not in cache:
                                        with open("/home/ec2-user/Graph-DB-for-music/event_analyze_result.json", "a") as f:
                                            f.write(json.dumps(result, default=str))
                                            f.write('\n')
                                    #print('yes')
                                        cache.add(json.dumps(result, default=str))
                                    cnt+=1
                                else:
                                    r = sp.get_artist_search(artist['name'])
                                    result['artistName'] = r['name']
                                    result['artistId'] = r['id']
                                    result['followers'] = r['followers']
                                    result['genre'] = r['genre']
                                    result['popularity'] = r['popularity']
                                    if json.dumps(result, default=str) not in cache:
                                        with open("/home/ec2-user/Graph-DB-for-music/event_analyze_result.json", "a") as f:
                                            f.write(json.dumps(result, default=str))
                                            f.write('\n')
                                        cache.add(json.dumps(result, default=str))
                                    cnt+=1
                                    #print('yes')

                                    
                            #print('Nope') 
                        print('Artist Page Finished : ', artist_info['name'], 'page : ', str(page), 'count : ', str(cnt), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                        time.sleep(3)   
                    except Exception as e:
                        print('Error Occured during event_analyze.py while : ', e)

                    page+=1

    except Exception as e:
        print('Error Occured during event_analyze.py : ', e)    


print('Finished for Prepared contents')

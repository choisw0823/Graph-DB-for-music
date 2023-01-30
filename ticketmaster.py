import requests
import json
import datetime

class TicketpyClient:
    def __init__(self):
        self.api_key = 'qRWaLa07WId3NRKnpPctYDX8iRCaVvpT'
        self.base_url = 'https://app.ticketmaster.com/discovery/v2/'

    #id, keyword, attractionId, venueId, startDateTime, endDateTime, city 
    def search_event(self, **kwargs):
        try:
            params = {'apikey': self.api_key}
            params.update(kwargs)
            response = requests.get(f'{self.base_url}events.json', params=params)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            return None

    def get_event_details(self, event_id):
        try:
            params = {'apikey': self.api_key}
            response = requests.get(f'{self.base_url}events/{event_id}.json', params=params)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            return None

    def search_attraction(self, **kwargs):
        try:
            params = {'apikey': self.api_key}
            params.update(kwargs)
            response = requests.get(f'{self.base_url}attractions.json', params=params)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            return None
    
    def get_attraction_details(self, attraction_id):
        try:
            params = {'apikey': self.api_key}
            response = requests.get(f'{self.base_url}attractions/{attraction_id}.json', params=params)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            return None
    
    def search_classification(self, **kwargs):
        try:
            params = {'apikey': self.api_key}
            params.update(kwargs)
            response = requests.get(f'{self.base_url}classifications.json', params=params)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            return None
    
    def get_classification_details(self, classification_id):
        try:
            params = {'apikey': self.api_key}
            response = requests.get(f'{self.base_url}classifications/{classification_id}.json', params=params)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            return None
    
    def get_genre_details(self, genre_id):
        try:
            params = {'apikey': self.api_key}
            response = requests.get(f'{self.base_url}genres/{genre_id}.json', params=params)
            return response.json()

        except requests.exceptions.RequestException as e:
            print(e)
            return None
    def get_segment_details(self, segment_id):
        try:
            params = {'apikey': self.api_key}
            response = requests.get(f'{self.base_url}segments/{segment_id}.json', params=params)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            return None

    def get_sub_genre_details(self, sub_genre_id):
        try:
            params = {'apikey': self.api_key}
            response = requests.get(f'{self.base_url}sub_genres/{sub_genre_id}.json', params=params)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            return None

    def search_venue(self, **kwargs):
        try:
            params = {'apikey': self.api_key}
            params.update(kwargs)
            response = requests.get(f'{self.base_url}venues.json', params=params)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            return None

    def get_venue_details(self, venue_id):
        try:
            params = {'apikey': self.api_key}
            response = requests.get(f'{self.base_url}venues/{venue_id}.json', params=params)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            return None
    
if __name__=='__main__':
    t = TicketpyClient()
    start = datetime.datetime(2022, 1, 1).strftime('%Y-%m-%dT%H:%M:%SZ')
    print(start)
    search = t.search_event(keyword='ed sheeran')
    #for i in range(1, search['page']['totalPages']):
    # with open('test', 'w') as f:
    #     f.write(json.dumps(search))
    #print(search)
    for event in search['_embedded']['events']:
        try:
        #print(event['name'], event['id'])
        #detail = t.get_event_details(event['id'])
        #print(json.dumps(detail))
            #print(event['name'], event['id'], event['dates']['start']['dateTime'], event['classifications'][0]['segment']['id'],  event['classifications'][0]['segment']['name'], \
                #event['classifications'][0]['genre']['id'],  event['classifications'][0]['genre']['name'],  event['classifications'][0]['subGenre']['id'],  event['classifications'][0]['subGenre']['name'], \
                #event['priceRanges'][0]['max'], event['priceRanges'][0]['min'], event['promoters'], event['_embedded']['venues'][0]['name'],  event['_embedded']['venues'][0]['id'],  event['_embedded']['venues'][0]['city']['name'], \
                     #event['_embedded']['venues'][0]['state']['name'],  event['_embedded']['venues'][0]['country']['name'],  event['_embedded']['venues'][0]['address'],  event['_embedded']['venues'][0]['location'])
            venue = t.get_venue_details(event['_embedded']['venues'][0]['id'])
            search_venue = t.search_venue(keyword='Maple Leaf Gardens')
            print(search_venue['_embedded']['venues'][0])
            print(venue['name'], venue['id'], venue['aliases'], venue['city'], venue['state'], venue['country'], venue['address'], venue['location'])
            # with open('test', 'w') as f:
            #     f.write(json.dumps(venue))
            break
            #print('\n')
        except Exception as e:
            print('Error : ', e)
    #print(json.dumps(t.get_event_events('vvG10Z9xpbkwb0')))
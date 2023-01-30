import requests
from bs4 import BeautifulSoup
import time
import json

class SongKickScraper:
    def __init__(self):
        self.url = "https://www.songkick.com"

    #Not completed function
    def get_artist_events(self, artist_name, page):
        search_url = self.url + "/search?query=" + artist_name + "&type=artists&page="+str(page)
        search_page = requests.get(search_url)
        search_soup = BeautifulSoup(search_page.content, "html.parser")
        #artist_url = search_soup.find("a", class_="link-to-artist").get("href")
        #artist_page = requests.get(artist_url)
        #artist_soup = BeautifulSoup(artist_page.content, "html.parser")
        #event_list = artist_soup.find("ol", class_="events-list")
        #print(search_soup)
        uri = search_soup.find('p', class_="summary").find('a').get('href')
        artist_url = self.url + uri + '/gigography'
        time.sleep(2) 
        artist_page = requests.get(artist_url) 
        artist_soup = BeautifulSoup(artist_page.content, "html.parser")
        
        # with open('test2', 'w') as f:
        #     f.write(str(artist_soup))
        
        time_list = []
        for t in artist_soup.find_all('time'):
            if t.get_text() != '':
                time_list.append(t.get_text())
        event_list = []

        for t in time_list:
            event_list.append(artist_soup.find('li', {'title':t}))
        #print(event_list[0])
        #event_list = artist_soup.find_all("ul", class_="event-listings artist-focus")
        events = []
        for event in event_list:
            print(event)
            print('\n')
            event_name = event.find("strong").get_text()
            event_date = event.find("time").get("datetime")
            event_location = event.find("span", class_="venue-name").get_text()
            a = event.find('p', class_='location')
        
            b = a.find_all('a')[1]

            c = b.find('span')
            d = c.get_text()
            #print(d)
            location_city = [i.strip() for i in d.split(',')]
            address = event.find('span', class_='street-address').get_text()

            d = {"name": event_name, "date": event_date, "location": event_location}
            if len(location_city)==3:
                d['city'] = location_city[0]
                d['state'] = location_city[1]
                d['country'] = location_city[2]
                d['address'] = address
            else:
                d['city'] = location_city[0]
                d['country'] =  location_city[1]
                d['address'] = address
            #print(d)
            #print('')
            events.append(d)
            
        return events
        
    def get_artist_events_json(self, artist_name, page):
        try:
            search_url = self.url + "/search?query=" + artist_name + "&type=artists"
            search_page = requests.get(search_url)
            search_soup = BeautifulSoup(search_page.content, "html.parser")
        #artist_url = search_soup.find("a", class_="link-to-artist").get("href")
        #artist_page = requests.get(artist_url)
        #artist_soup = BeautifulSoup(artist_page.content, "html.parser")
        #event_list = artist_soup.find("ol", class_="events-list")
        #print(search_soup)
            uri = search_soup.find('p', class_="summary").find('a').get('href')
            artist_url = self.url + uri + '/gigography' + '?page='+str(page)
            time.sleep(2) 
            artist_page = requests.get(artist_url) 
            artist_soup = BeautifulSoup(artist_page.content, "html.parser")
        
        # with open('test2', 'w') as f:
        #     f.write(str(artist_soup))
            events = []
            # time_list = []
            page_info = artist_soup.find('div', {'role':'navigation'})
            total_page = 0

            pg = page_info.find_all('a')

            total_page = int(pg[-2].get('aria-label').split()[1])
            
            for event in artist_soup.find_all('script', {'type':'application/ld+json'}):
                js = event.get_text()
                events.append(json.loads(js)[0])
        
            return (events, total_page)

        except Exception as e:
            print('Error Occured during sonkick.py get_artist_events_json() : ', e)
            return None
        
    
if __name__=='__main__':
    S = SongKickScraper()
    events, total_page = S.get_artist_events_json('ed sheeran', 1)
    #print(events)
    print(events[0]['name'], events[0]['startDate'], events[0]['endDate'], events[0]['location']['address'], events[0]['location']['name'], events[0]['location']['geo'], \
        events[0]['performer'][0]['name'])
    print(events[0]['location']['geo']['longitude'], events[0]['location']['geo']['latitude'])
    print(events[0]['location']['address']['addressLocality'], events[0]['location']['address']['addressCountry'], events[0]['location']['address']['streetAddress'], events[0]['location']['address']['postalCode'])
    print(total_page)
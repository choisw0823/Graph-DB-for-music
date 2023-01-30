import requests
import json

class DiscogsAPI:
    def __init__(self):
        self.key = "OqHqVuXdhGxJXKVdVKOm"
        self.secret = "gQOdvWbiYbeacPZiiiFffcACbqMwWLFg"
        self.user_agent = "infolabGraphdb/1.0"
        self.token = "kismxtDjDoJFhaAVtPNdJUHYBQurLAzudbJVgZOo"
        self.base_url = "https://api.discogs.com/database"
    
    def make_request(self, endpoint, params={}):
        headers = {"User-Agent": self.user_agent}
        url = f"{self.base_url}{endpoint}"
        try:
            params['key'] = self.key
            params['secret'] = self.secret
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as errh:
            print ("HTTP Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("Something went wrong",err)
            
    def search(self, query, type='artist', per_page=50):
        endpoint = "/search"
        params = {
            "q": query,
            "type": type,
            "per_page": per_page
        }
        return self.make_request(endpoint, params)
    
    def get_community_release_rating(self, release_id):
        endpoint = f"/releases/{release_id}/rating"
        return self.make_request(endpoint)
    
    def get_release_stats(self, release_id):
        endpoint = f"/releases/{release_id}/statistics"
        return self.make_request(endpoint)
    
    def get_artist(self, artist_id):
        endpoint = f"/artists/{artist_id}"
        return self.make_request(endpoint)
    
    def get_artist_releases(self, artist_id, per_page=50):
        endpoint = f"/artists/{artist_id}/releases"
        params = {
            "per_page": per_page
        }
        return self.make_request(endpoint, params)
    
    def get_label(self, label_id):
        endpoint = f"/labels/{label_id}"
        return self.make_request(endpoint)
    
    def get_label_releases(self, label_id, per_page=50):
        endpoint = f"/labels/{label_id}/releases"
        params = {
            "per_page": per_page
        }
        return self.make_request(endpoint, params)
    
    def get_price_suggestions(self, release_id):
        endpoint = f"/marketplace/price_suggestions/{release_id}"
        return self.make_request(endpoint)




if __name__=='__main__':
    # Discog = DiscogsClient()
    # r = Discog.search('Charlie Puth', 'artist')
    # a = list(r)
    # print(a)
    # r1 = Discog.get_artist(4061019)
    # #r2 = Discog.get_artist_releases(4061019)
    # print(r1)
    # print(r2)
    # q = 1
    # while(q != '0'):
    #     input('num(1 : get_artist, 2 : get_artist_releases, 3 : get_rellease , 4 : get_label, 5 : get_label_releases, 6 : get_price_suggestion, 7 : get_releases_statistics, 8 :  ')
    Discog = DiscogsAPI()
    print(json.dumps(Discog.search(query='Charlie puth', type='artist', per_page=3)))
    print(json.dumps(Discog.search(query='Charlie puth', type='artist', per_page=3)))
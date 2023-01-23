import spotipy
from spotipy.oauth2 import SpotifyClientCredentials



class spotify:
    def __init__(self):
        client_credentials_manager = SpotifyClientCredentials(client_id='3e87f4298e374c6eab7a412786b8599e', client_secret='871408c7e3544a0ca3eaec30697d7334')
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def get_id(self,name, type):
        if (type=='artist'):
            return self.sp.search(q=name, type=type, limit=1)['artists']['items'][0]['id']
        elif (type=='track'):
            return self.sp.search(q=name, type=type, limit=1)['tracks']['items'][0]['id']
        elif (type=='album'):
            return self.sp.search(q=name, type=type, limit=1)['albums']['items'][0]['id']
    
    

if __name__=='__main__':
    sp = spotify()
    print(sp.sp.search(q='One call away', type='track'))
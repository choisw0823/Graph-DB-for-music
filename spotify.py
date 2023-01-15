import spotipy
from spotipy.oauth2 import SpotifyClientCredentials



class spotify:
    def __init__(self):
        client_credentials_manager = SpotifyClientCredentials(client_id='3e87f4298e374c6eab7a412786b8599e', client_secret='871408c7e3544a0ca3eaec30697d7334')
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


if __name__=='__main__':
    sp = spotify()
    print(sp.sp.search(q='I\'m outta love', type='track'))
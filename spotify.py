import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json


class spotify:
    def __init__(self):
        client_credentials_manager = SpotifyClientCredentials(client_id='3e87f4298e374c6eab7a412786b8599e', client_secret='871408c7e3544a0ca3eaec30697d7334')
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def get_id(self,name, type):
        if (type=='artist'):
            try:
                return self.sp.search(q=name, type=type, limit=1)['artists']['items'][0]['id']
            except Exception as e:
                print('Error occured during get_id(artist): ', e)
                return None
        elif (type=='track'):
            try:
                info = self.sp.search(q=name, type=type, limit=1)
                print('rate : ', self.sp.rate_limiting)
                return {'artist':info['tracks']['items'][0]['artists'][0]['id'], 'track' : info['tracks']['items'][0]['id']}
            except Exception as e:
                print('Error occured during get_id(track): ', e)
                return None
                
        elif (type=='album'):
            try:
                return self.sp.search(q=name, type='track', limit=1)['tracks']['items'][0]['album']['id']
            except Exception as e:
                print('Error occured during get_id(album): ', e)
                return None
    
    def get_info(self, values):
        try:
            ret = {'track':None, 'artist':[], 'album':None, 'feature':None}
            track_info = self.sp.search(q=values['title'], type='track', limit=1)
            artist_info = self.sp.search(q=values['artist'], type='artist', limit=1)
            album_info = None
            for artist in  track_info['tracks']['items'][0]['artists']:
                if artist['id'] == artist_info['artists']['items'][0]['id']:
                    artists_info = self.sp.artists([i['id'] for i in track_info['tracks']['items'][0]['artists']])
                    album_info = self.get_album_info(track_info['tracks']['items'][0]['album']['id'])
                    audio_feature = self.get_audio_features(track_info['tracks']['items'][0]['id'])

                    ret['track'] = {'id':track_info['tracks']['items'][0]['id'], 'name':track_info['tracks']['items'][0]['name'], 'popularity':track_info['tracks']['items'][0]['popularity'], 'release_date':track_info['tracks']['items'][0]['album']['release_date']}
                    ret['artist'] = [{'id':i['id'],'name': i['name'], 'followers': i['followers']['total'], 'genre':i['genres'], 'popularity': i['popularity']} for i in artists_info['artists']]
                    ret['album'] = {'type':album_info['album_type'], 'id':album_info['id'], 'name':album_info['name'], 'popularity':album_info['popularity'], 'release_date':album_info['release_date']}
                    ret['feature'] = {'danceability':audio_feature[0]['danceability'], 'energy':audio_feature[0]['energy'],'loudness':audio_feature[0]['loudness'],'valence':audio_feature[0]['valence'],'tempo':audio_feature[0]['tempo']}
                    
                    return ret
            return None
        except Exception as e:
            print('Error Occured during get_info : ', e)
            return None

       

    def get_track_info(self, track_id):
        return self.sp.track(track_id)

    def get_album_info(self, album_id):
        return self.sp.album(album_id)

    def get_artist_info(self, artist_id):
        return self.sp.artist(artist_id)

    def get_audio_features(self, track_id):
        return self.sp.audio_features(track_id)


if __name__=='__main__':
    sp = spotify()
    print(sp.sp.search(q='One call away', type='track'))
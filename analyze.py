import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
user_id = os.getenv('SPOTIPY_USER_ID')
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def getTrackId(track_name):
    try:
        search_id = sp.search(track_name, limit=1, offset=0, type='track', market=None)["tracks"]["items"]
        track = search_id[0]
        track_id = track["id"]
        return track_id

    except IndexError:
        print("IndexError has occurred!")
    except AttributeError:
        print("AttributeError has occurred!")

def getAudioFeature(track_id):
    try:
        features = sp.audio_features(track_id)
        for feature in features:
          return feature

    except IndexError:
        print("IndexError has occurred!")
    except AttributeError:
        print("AttributeError has occurred!")


def getRecommendTracks(track_id):
    try:
      playlist_features = []
      danceabilitys = []
      # プレイリストの特徴量を検出
      result = sp.user_playlist(user_id, '37i9dQZF1E35r4Op1DJzHt')

      for track in result['tracks']['items']:
        playlist_id = track['track']['id']
        playlist_features.append(getAudioFeature(playlist_id))

      # 取得曲の特徴量を検出
      track_feature = getAudioFeature(track_id)

      for playlist_feature in playlist_features:
        if track_feature['danceability'] > 0.56:
            if (track_feature['danceability']-1) <= playlist_feature['danceability'] <= (track_feature['danceability']+1) and \
                (track_feature['energy']-0.1) <= playlist_feature['energy'] <= (track_feature['energy']+0.1):
                match = sp.track(playlist_feature['id'])
                return "ノリノリなあなたには" + match['name'] + "もおすすめです！"

        elif track_feature['mode'] == 0:
          if (track_feature['acousticness']-0.1) <= playlist_feature['acousticness'] <= (track_feature['acousticness']+0.1) and playlist_feature['mode'] == 0:
              match = sp.track(playlist_feature['id'])
              return "ムーディなあなたにはこちら！" + match['name']

        else :
          return "にゃーん"

    except IndexError:
        print("IndexError has occurred!")
    except AttributeError:
        print("AttributeError has occurred!")

if __name__ == '__main__':
    track_id = getTrackId("butter")
    track_id = getTrackId("future nova")
    print(getRecommendTracks(track_id))
    